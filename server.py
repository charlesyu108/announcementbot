from flask import Flask, request
import requests, json
app = Flask(__name__)

BOT_URL = "https://api.groupme.com/v3/bots/post"
BOT_ID = "723d5f0c594795227d2965578c"

#id":"151279007731713032","name":"Charles Yu","sender_id":"30153727"

@app.route("/")
def index():
    return "This is the index."

@app.route("/bot", methods = ["POST"])
def hello():

    data = json.loads(request.data)

    # if "@Announce" in data["text"]:
    #     message = {
    #     "text" : "WOOT it works!",
    #     "bot_id" : BOT_ID
    #     }
    #
    #     res = requests.post(BOT_URL, data = message)
    #
    #     print 'response from server: ', res

    if "@Announce" in data["text"]:

        message = {"message":{
        "source_guid" : "GUID",
        "recipient_id" "151279007731713032"
        "text" : "WOOT it works!",
        # "id" : BOT_ID
        }}

        res = requests.post("https://api.groupme.com/v3/direct_messages", data = message)

        print 'response from server: ', res.text

    return "Hello world!"

if __name__ == '__main__':
    app.run(debug=True)
