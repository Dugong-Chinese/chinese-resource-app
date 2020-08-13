from flask import Blueprint, request
from flask_restful import Resource, Api
import math
import jieba
import requests
from bs4 import BeautifulSoup


blank_exercises = Blueprint(
    "fill_in_the_blank",
    __name__,
    static_folder=".../build",
    static_url_path="/",
    url_prefix="/api/",
)

api = Api(blank_exercises)


class FillInTheBlank(Resource):
    """Sends fill in the blank exercises. Currently supports Simplified Chinese."""

    # NOTE: inelegant, web-scraping solution. Ideally we would have our own program for generating exercises
    # down the line, have our own database of vocabulary and sentences (which will be searched *much* more quickly)
    # or work out some sort of deal with PurpleCulture to not have our IP address banned if that issue ever arises.

    def get(self):
        """Example usage: http://localhost:5000/api/fillin?hanzi=%E5%96%9C%E6%AC%A2&amount=5&limit=0.7 (~20 sec to load)"""
        args = request.args
        phrase = args["hanzi"]
        amount = int(args["amount"])
        difficulty_limit = float(args["limit"])

        exercises = generate_exercises(phrase, amount, difficulty_limit)

        return {"exercises": exercises}


def generate_exercises(hanzi_phrase: str, amount=5, difficulty_limit=0.7):
    """Generates fill in the blank exercises."""

    # NOTE: currently using an example document with known user text. This would be changed
    # to instead access the user's known vocabulary in the database, and this code would
    # have to be updated to match this in that case. We should add a username argument
    # to the get request above and have the database search that user's vocabulary in this
    # function.

    # IMPORTANT: takes a while to load, because scraping and accessing the web pages isn't fast.
    # We should probably introduce a loading bar or have this run in the background for users.

    try:
        file = open("exercises/sample_vocabulary.txt", "r")

    except FileNotFoundError:
        file = open("sample_vocabulary.txt", "r")

    words = file.readlines()

    known_vocab = set()

    for i in range(len(words)):
        known_vocab.add(words[i][: len(words[i]) - 1])

    # add some punctuation as well

    known_vocab.add("。")
    known_vocab.add("，")
    known_vocab.add("：")
    known_vocab.add("；")
    known_vocab.add("-")
    known_vocab.add("？")
    known_vocab.add("！")
    known_vocab.add(" ")
    known_vocab.add("_")
    known_vocab.add("'")
    known_vocab.add('"')

    file.close()

    # Purple Culture supports different ways of looking up sentences - you can either look up
    # sentences that *contain* n words, or you can find sentences that have n words - in a row.

    purple_phrase = ""
    for i in range(len(hanzi_phrase)):
        if i != len(hanzi_phrase) - 1:
            purple_phrase += hanzi_phrase[i] + "+"
        else:
            purple_phrase += hanzi_phrase[i]

    # jukuu is quite slow, but it has simpler sentences more suited to beginners
    output = []
    for x in range(10):
        try:
            # searching jukuu for sentences
            response = requests.get(
                f"http://jukuu.com/show-{hanzi_phrase}-{x}.html", timeout=25
            )
            soup = BeautifulSoup(response.content, "html.parser")

            data = soup.find_all("tr")
            linked_output = []

            # jukuu supports the english meaning and 汉字
            for tr in data:
                if tr.has_attr("class"):
                    if list(tr["class"])[0] == "e" or list(tr["class"])[0] == "c":
                        try:
                            linked_output.append(list(tr.children)[1].text.strip())
                        except:
                            linked_output = [list(tr.children)[1].text.strip()]

                if len(linked_output) == 2:
                    output.append(linked_output)
                    linked_output = []

        except:
            pass

    # create soup and get number of results
    response = requests.get(
        f"https://www.purpleculture.net/sample-sentences/?word={purple_phrase}&page={1}"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    num_results = math.ceil(
        int(
            list(soup.findAll("div", {"class": "card-header"})[0].children)[
                1
            ].text.split()[5]
        )
        / 20
    )

    # limit maximum results searched, otherwise could take forever for simpler exercises
    if num_results > 30:
        num_results = 30

    answer = []

    for i in range(num_results):
        response = requests.get(
            f"https://www.purpleculture.net/sample-sentences/?word={purple_phrase}&page={i}"
        )
        soup = BeautifulSoup(response.content, "html.parser")

        answer = soup.find_all("li", {"class": "pb-4"})

    # holds all hanzi and pinyin for
    true_answer = []
    for sentence in answer:
        full_sentences = []
        full_sentences.append(list(sentence.children)[3].text.strip())
        pinyin = ""
        hanzi = ""

        for x in range(len(list(sentence.children)[0]) - 1):
            pinyin += list(list(list(sentence.children)[0].children)[x].children)[
                0
            ].text.strip()
            hanzi += list(list(list(sentence.children)[0].children)[x].children)[
                1
            ].text.strip()

        full_sentences.append(hanzi)
        full_sentences.append(pinyin)

        true_answer.append(full_sentences)

    # known words in each example sentence
    words_known = {}

    # known words in purple culture
    p_words_known = {}

    for i in range(len(output)):
        words_known[i] = [
            len(set(known_vocab) & set([ele for ele in jieba.cut(output[i][1], cut_all=False)])) / len([ele for ele in jieba.cut(output[i][1], cut_all=False)]),
            output[i][1],
        ]

    result = reversed(sorted(words_known.items(), key=lambda x: x[1][0]))

    for i in range(len(true_answer)):
        p_words_known[i] = [
            len(set(known_vocab) & set(true_answer[i][1])) / len(true_answer[i][1]),
            true_answer[i][1],
            true_answer[i][2],
        ]

    result2 = reversed(sorted(p_words_known.items(), key=lambda x: x[1][0]))

    result2 = [ele for ele in result2]

    result = [ele for ele in result]

    result += result2

    result = reversed(sorted(result, key=lambda x: x[1][0]))
    result = [ele for ele in result]

    # gather useful sentences (only save those within difficulty range)
    possible_exercises = []
    for i in range(len(result)):
        if result[i][1][0] >= float(difficulty_limit):
            possible_exercises.append(result[i][1])

    if len(possible_exercises) == 0:
        possible_exercises.append(result[0][1])

    # generate the list that will be returned for the API
    return_lst = []
    for challenge in possible_exercises:
        blank_hanzi = challenge[1]
        return_sublst = []
        for i in range(len(hanzi_phrase)):
            for x in range(len(hanzi_phrase[i])):
                replace_with = " _ " * len(hanzi_phrase[i])
                blank_hanzi = blank_hanzi.replace(hanzi_phrase[i], replace_with)

        # depending on whether it is from jukuu or purpleculture it will/won't have pinyin
        if len(challenge) >= 3:
            return_sublst.append(round(challenge[0], 3))
            return_sublst.append(blank_hanzi)
            return_sublst.append(challenge[2])
        else:
            return_sublst.append(round(challenge[0], 3))
            return_sublst.append(blank_hanzi)

        return_lst.append(return_sublst)

    return {"exercises": return_lst}


api.add_resource(FillInTheBlank, "fillin")
