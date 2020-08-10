# grab the list of all the resources at https://challenges.hackingchinese.com/resources
import requests, json
from bs4 import BeautifulSoup

# links that hold the correct content, not headers and other HTML
true_links = []


def extract_resources(page: int) -> None:
    page = requests.get(
        f"https://challenges.hackingchinese.com/resources/stories?page={page}"
    )

    soup = BeautifulSoup(page.content, "html.parser")

    # links are stored within a unique <h4> header on each card
    links = soup.find_all("h4")

    for i in range(len(links)):
        try:
            if links[i]["class"] == ["card-title"]:
                true_links.append(links[i])
        except:
            pass


for i in range(1, 10):
    extract_resources(i)  # 9 different pages with info

file = open("links.json", "w+")

count = 0
data = []
for i in range(len(true_links)):
    try:
        # ensure it is a working link
        response = requests.get(
            str(list(true_links[i].children)[0]["href"]),
            timeout=5,
            allow_redirects=True,
            stream=True,
        )
        if response != 404:
            count += 1
            data.append(
                {
                    "id": count,
                    "link": str(list(true_links[i].children)[0]["href"]),
                    "vocab_link": "",  # must be done manually
                    "name": str(list(true_links[i].children)[0].text),
                    "tags": [], # must be done manually
                    "upvotes": 0,
                    "rating": -1, # represents no rating present
                    "images": [] # images used for cover, card preview, etc.
                }
            )

            # file.write(str(list(true_links[i].children)[0]['href']) + '\n')

    except:  # Connection Refused
        pass

json.dump(data, file)

file.close()
