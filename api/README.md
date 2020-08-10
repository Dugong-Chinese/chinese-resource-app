# chinese-resource-app

## Database
**Important:** read this section when pulling in order to have a functional database for use with the API.

### When pulling
First time pulling:
- Take a look at `local_settings_example.py` and fill in the database information; follow the instructions in the
 docstring of the module. You may need to create a database at this point, and point the configuration to it.

On any pull, including the first one:
1. Make sure you installed the requirements from `requirements.txt`, as these contain the necessary drivers and may
 contain important updates.
1. Run `flask db upgrade` to apply migrations to your local database.

### When developing
1. After modifying the database models, run `flask db migrate`. Add the `-m "Commit message"` option as you would for a
 Git commit, modifying the commit message as appropriate. Treat these as commits for the database.
1. Run `flask db upgrade` to apply the migration to your own local database.
    - If you add a new not-nullable column on an existing module, it's possible you'll have to input a default for
     existing data (even if there is no actual record in the table on your local database). In this case, always prefer
     adding a default to the model itself, unless the value cannot be assumed. In the latter case, consider if it makes
     sense to allow the column to be nullable. Both this and the previous approach have potentially long-lived
     consequences.
1. Make sure to push any changes that will automatically have occurred in the `migrations` directory: all contributors
 need to have up-to-date database schemata.


## REST api

### Intro
We will be using `Flask` and `flaskRESTful` for the backend. This makes it very easy to setup a backend that can accept
 HTTP requests.

The `api.py` is where the app will be run and json will be read/sent, but we can use other files and just import them in
 the main `api.py` file.

`Flask` runs on http://localhost:5000. We can use this to test the various HTTP requests with `curl`.

### `curl` details
`curl` is a great package used for "transferring data with URLs". You most likely have it installed, but in case you
 don't you can easily go their website and install it with instructions and a download wizard
 [here](https://curl.haxx.se/dlwiz/?type=bin).

### No Authorization
Below are a few examples of how the Flask app would work without authorization for the API.

#### GET request
By running the following command from the terminal, you can perform a simple GET request from the website of your choice
 (we'll be using http://localhost:5000):

`curl http://localhost:5000/test`

In the `api.py` file we already have an example URL set up, which will return "Hello World!". You can see that if we run
 the above command then we get the expected output:
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

Everything up to the URL is mandatory in order to have the data be sent and parsed correctly. Afterwards, we include the
 URL to wherever it is that we want to POST the data, and then add the data with the `-d` flag and the data that we want
  to send. In this case, the Flask route will just echo whatever is being sent to it, returning:
```
{
    "you sent": {
        "name": "Alice"
    }
}
```
### Authorization
Secure authorization is important so that people can't just go to the API link and find everyone's usernames, passwords, and other sensitive data. So, we will use `flask_jwt` and `werkzeug` to encode tokens and use those so that only registered admin users can view the sensitive data.

#### Step 1 - The Database
First of all, we need to generate a database of users and their passwords. We can do this is a simple list in Python. An example is below:
```
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcdwxyz'),
]
```
All of the users will be able to login with their usernames and passwords to view the API.

#### Step 2 - App Config Key
To make it as secure as we can, we need to set an app config key. This can be done in one line; the key should be long, not guessable, and stored in an environment variable.

```
app.config['SECRET_KEY'] = 'super-secret'
```
*Look at how secure that key is (hint: it's not)! We should move it onto an environment variable eventually.*

Ideally, this would be an environment variable or the repo would be private so that it wouldn't be publicly accessible.

#### Step 3 - Modified Requests
For each URL and all the HTTP requests below it, we can choose whether it is public or private (requiring the admin token). If it's public, nothing changes from the above. However, if it is private, then we need to add `decorators = [checkuser, jwt_required()]` just below the class name.

#### Step 4 - Getting Authentication
You need to have a token in order to access the admin pages, but it'd be tricky for users to remember the entirety of the token. So, what happens is that they first send their username and password to `/auth`, which will give them the token unique to their user id.

Example:
```
curl -H "Content-Type: application/json" -X POST \
'{"username":"user1","password":"abcxyz"}' http://localhost:5000/auth
```
If their username and password is correct, they will get back something that looks like this (but larger of course):
```
{
  "access_token": "eyJ0i....DPcYY"
}
```

#### Step 5 - Using the Token
Now that the user has their access token, they can perform requests to protected URLs. This is done with the header "Authorization" and key "jwt \<token\>". Curl example below:
```
curl -H "Authorization: jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTY0NDY1OTgsImlhdCI6MTU5NjQ0NjI5OCwibmJmIjoxNTk2NDQ2Mjk4LCJpZGVudGl0eSI6MX0.EcWlrWFIEI-nzh1mYIKqpTjLU0GMgaqSpXIf_eUJ1G4" http://localhost:5000/api/test
```
This will get the user back: *Hello, user1*, assuming they are user1, since JWT supports finding out which user called the request. POST, DELETE, PUT, etc. requests work the exact same way, they just always require the "Authorization: jwt \<token\> header.

*Note: it's safe to share the tokens above because one benefit of JWT is that the tokens are being refreshed every few minutes. Eventually, this means that we should automate the admin request - we can have them input username, password, and protected url they want to go to, and then generate the authentication from username and password.*

#### Full Vanilla JS Example
1. Getting Authentication
```
fetch("/auth",
{
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    method: "POST",
    body: JSON.stringify({username: "user1", password: "abcxyz"})
})
.then(res => res.json()).then(data => {
      console.log(data)})
.catch(function(res){ console.log(res) })
```

We get `{access_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1O…I6MX0.ImrPq4HC3f5_6yHWueBsI0fQfCbnISvF-rP3nQIapG4"}`, let's copy and paste the token (**without** brackets).

*Note: the above token is **not** the full token. You need to click on the response and it will show you the full token, that is why there are the three . in the access token above - it's been shortened!*

2. Perform Request *without* token (failure)
```
fetch('/api/test')

VM1842:1 GET http://localhost:3000/api/test 401 (UNAUTHORIZED)
```

We can see that it is unauthorized because we didn't provide proper credentials. Let's try again.

3. Perform Request *with* token (success)
```
fetch('/api/test', {
    headers: {
        'Authorization': 'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTY0NDk2MTgsImlhdCI6MTU5NjQ0OTMxOCwibmJmIjoxNTk2NDQ5MzE4LCJpZGVudGl0eSI6MX0.UI374UJLdBwd8csAW9AJTClv92G1R6b9Lr67TPFgazk'
    }

}).then(res => res.json()).then(data => {
      console.log(data)})

VM2431:7 {response: "Hello user1!"}
```
We get the response that we expected.

To conclude, HTTP requests with JWT are a breeze and we need to incorporate it for sensitive data.
