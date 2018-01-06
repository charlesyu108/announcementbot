from flask import Flask, request, redirect, url_for, render_template, make_response
import requests, json, time
from bot import AnnouncementBot
from reseed import ContactUpdater

app = Flask(__name__)

BOT_ID = "723d5f0c594795227d2965578c" # Bot ID of whoever is listening in
ACCESS_TOK = "sWNFUhEiTLajKC9R3rnEblOx13o1yc5anbCqswp3" # BeezleGuy12's access tok
APP_REDIRECT = 'https://oauth.groupme.com/oauth/authorize?client_id=z5v5YAeP1rVo2pT4b95mEWlfpztGGs3OYfx1V8fjltbmUtvV'
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
    return redirect(updater.authenticate())

@app.route("/authenticate_result", methods = ["GET"])
def auth_approved():
    u_auth_tok = request.args.get("access_token")
    if not u_auth_tok:
        return redirect(url_for('authenticate'))
    groups = updater.getGroups(u_auth_tok)
    resp = make_response(render_template("update.html", groups = groups))
    resp.set_cookie('groups', json.dumps(groups))

    # TODO cookies have a limit of 2000 figure out what to do...
    return resp
    # return render_template("update.html", groups = groups)
    # return "OK - User authenticated"

@app.route("/group_selected",  methods = ["GET"])
def select():

    print request.cookies.get("groups"), len(request.cookies.get("groups"))
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
