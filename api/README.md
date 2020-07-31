# chinese-resource-app
## REST api

### Intro
We will be using `Flask` and `flaskRESTful` for the backend. This makes it very easy to setup a backend that can accept HTTP requests.

The `api.py` is where the app will be run and json will be read/sent, but we can use other files and just import them in the main `api.py` file.

`Flask` runs on http://localhost:5000. We can use this to test the various HTTP requests with `curl`.

### `curl` details
`curl` is a great package used for "transferring data with URLs". You most likely have it installed, but in case you don't you can easily go their website and install it with instructions and a download wizard [here](https://curl.haxx.se/dlwiz/?type=bin).

#### GET request
By running the following command from the terminal, you can perform a simple GET request from the website of your choice (we'll be using http://localhost:5000):
`curl http://localhost:5000/test`

In the `api.py` file we already have an example URL set up, which will return "Hello World!". You can see that if we run the above command then we get the expected output:
```
{
    "response": "Hello World!"
}
```

We can also perform more complex GET requests with parameters as so:
`curl http://localhost:5000/multiply/20`

Which, likewise, returns what we'd expect it to:
```
{
    "result": 200
}
```
#### POST requests
POST requests are a bit trickier, but they're still manageable. Here's an example:
`curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:5000/test -d '{"name": "Alice"}'`

Everything up to the URL is mandatory in order to have the data be sent and parsed correctly. Afterwards, we include the URL to wherever it is that we want to POST the data, and then add the data with the `-d` flag and the data that we want to send. In this case, the Flask route will just echo whatever is being sent to it, returning:
```
{
    "you sent": {
        "name": "Alice"
    }
}
```