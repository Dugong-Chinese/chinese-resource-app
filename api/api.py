from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# GET request, no parameters
class SimpleExample(Resource):
    """
    Demonstrates simple GET + POST requests.
    """

    def get(self):
        # simply have the function name be 'get' and return a dict with the name ("response") and the text that you will send
        return {"response": "Hello World!"}

    def post(self):
        # get POST data with request.get_json()
        some_json = request.get_json()  # whatever was posted
        return {"you sent": some_json}


class ComplexExample(Resource):
    """
    Demonstrates a GET request with parameters.
    """

    def get(self, num):  # unlimited number of arguments
        return {"result": num * 10}


# link resources to their respective URLs
api.add_resource(SimpleExample, "/test")
# whatever you call the parameter will be the way that it needs to be invoked, for example here it would be e.g. ...?num=5
api.add_resource(
    ComplexExample, "/multiply/<int:num>"
)  # specify variable type (or typecast)

# you can start the server by cding to the directory and running python3 api.py; it will start on localhost:5000 (if not in use)
