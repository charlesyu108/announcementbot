from flask import Flask, request
import requests, json, time
from bot import AnnouncementBot
from reseed import ContactUpdater

app = Flask(__name__)

BOT_ID = "723d5f0c594795227d2965578c" # Bot ID of whoever is listening in
ACCESS_TOK = "sWNFUhEiTLajKC9R3rnEblOx13o1yc5anbCqswp3" # BeezleGuy12's access tok
APP_REDIRECT = 'https://oauth.groupme.com/oauth/login_dialog?client_id=dRAJHyBwkjycSjEPf6DBZqvtVy6LQM0AJ9gusQ1QxUwm0kSe'
GROUPME_API = "https://api.groupme.com/v3"

#id":"151279007731713032","name":"Charles Yu","sender_id":"30153727"

contacts = ["30153727"] #just me

bot = AnnouncementBot(ACCESS_TOK, BOT_ID, contacts)
updater = ContactUpdater(APP_REDIRECT)

@app.route("/", methods = ["POST"])
def onMessage():

    message = json.loads(request.data)

    if message['sender_type'] != 'bot':

        bot.send_announcement(message)

    return "OK"

@app.route("/authenticate", methods = ["GET"])
def authenticate():
    return redirect(APP_REDIRECT)

@app.route("/authenticate_result", methods = ["GET"])
def auth_approved():
    u_auth_tok = request.args.get("access_token")
    getgroups_res = requests.get(GROUPME_API + "/groups", params = {"token":u_auth_tok})
    print getgroups_res.text

    #TODO Need to prettify output as hyperlinks on which group to select.
    
    return "OK - User authenticated"

if __name__ == '__main__':
    app.run(debug=True)
