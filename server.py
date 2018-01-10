from flask import Flask, request, redirect, url_for, render_template, make_response
import requests, json, time, csv, os
from bot import AnnouncementBot
from reseed import ContactUpdater
from loader import ContactLoader

app = Flask(__name__)

def load_env_var(var):
    v = os.environ.get(var, None)
    if not v:
        raise ValueError('You must have "{}" variable'.format(var))
    return v

GROUPME_API = "https://api.groupme.com/v3"
BOT_ID = load_env_var('BOT_ID')
ACCESS_TOK = load_env_var('ACCESS_TOK')
APP_REDIRECT = load_env_var('APP_REDIRECT')

contactLoader = ContactLoader("contacts.csv")
contacts = contactLoader.load_contacts()
bot = AnnouncementBot(ACCESS_TOK, BOT_ID, contacts)
updater = ContactUpdater(APP_REDIRECT)

def reload_contacts():
    global contacts
    contacts = contactLoader.load_contacts()
    global bot
    bot = AnnouncementBot(ACCESS_TOK, BOT_ID, contacts)

@app.route("/", methods = ["GET"])
def index():
    return "AnnouncementBot 2.0"

@app.route("/contacts", methods = ["GET"])
def viewContacts():
    contact_string = " "
    for c in contacts:
        contact_string += (c + "\n")
    return "Current contact ID's: \n {}".format(contact_string)

@app.route("/listen", methods = ["POST"])
def onMessage():
    message = json.loads(request.data)
    if message['sender_type'] != 'bot':
        bot.send_announcement(message)

    return "OK"

@app.route("/reseed", methods = ["GET"])
def authenticate():
    return redirect(updater.authenticate())

@app.route("/reseed/authenticate_result", methods = ["GET"])
def auth_approved():
    u_auth_tok = request.args.get("access_token")
    if not u_auth_tok:
        return redirect(url_for('authenticate'))
    groups = updater.getGroups(u_auth_tok)

    return render_template("update.html", groups = groups)

@app.route("/reseed/select_group",  methods = ["POST"])
def select():
    members = json.loads(request.form["members"])
    try:
        contactLoader.export_contacts(members)
        bot.notify_control("The AnnouncementBot contact list has been successfully updated. {} members total.".format(len(members)))
        reload_contacts()
    except:
        bot.notify_control("WARNING: An error occurred reseeding AnnouncementBot. Please try again.")

    return "OK -- Check control group to make sure request went through..."

if __name__ == '__main__':
    app.run(debug=True)
