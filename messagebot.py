from flask import Flask, request
import requests, json
app = Flask(__name__)

BASE_URL = "https://api.groupme.com/v3/"
ACCESS_TOK = "sWNFUhEiTLajKC9R3rnEblOx13o1yc5anbCqswp3"

#30153727  ///":"151279007731713032","name":"Charles Yu","sender_id":"30153727"

@app.route("/")
def index():
    return "This is the index."

@app.route("/bot", methods = ["POST"])
def hello():

    data = json.loads(request.data)

    if "Ok" in data["text"]:

        message = {
        "message":{
        "source_guid" :'{}-{}-{}'.format("announcement-bot", "30153727", time.time()),
        # "recipient_id": "30153727", #9304534
        "recipient_id": "9304534", #9304534
        "text" : "You've just been beezed!"
        }}

        res = requests.post("https://api.groupme.com/v3/direct_messages", json = message, params = {"token": ACCESS_TOK})
        print res.url

        print 'response from server: ', res.text

    return "Hello world!"

if __name__ == '__main__':
    app.run(debug=True)
