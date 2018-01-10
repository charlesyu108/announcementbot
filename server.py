from flask import Flask, request, redirect, url_for, render_template, make_response
import requests, json, time, csv, os
from bot import AnnouncementBot
from reseed import ContactUpdater
from flask_sqlalchemy import SQLAlchemy

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
# POSTGRES_URL = load_env_var("POSTGRES_URL")
# POSTGRES_USER = load_env_var("POSTGRES_USER")
# POSTGRES_PW = load_env_var("POSTGRES_PW")
# POSTGRES_DB = load_env_var("POSTGRES_DB")

# DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
DB_URL = load_env_var("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)

from models import Member

try:
    contacts = Member.query.all()
except:
    contacts = []

contact_ids = [c.user_id for c in contacts]
bot = AnnouncementBot(ACCESS_TOK, BOT_ID, contact_ids)
updater = ContactUpdater(APP_REDIRECT)

def update_globals():
    global contacts
    contacts = Member.query.all()
    global bot
    contact_ids = [c.user_id for c in contacts]
    bot = AnnouncementBot(ACCESS_TOK, BOT_ID, contact_ids)

@app.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    print('Creating tables.')
    db.create_all()
    print('Shiny!')

@app.route("/", methods = ["GET"])
def index():
    return "AnnouncementBot 2.0"

@app.route("/contacts", methods = ["GET"])
def viewContacts():
    contact_string = " "
    for c in contacts:
        contact_string += (c.user_id + " ")
    return "Current contacts: \n {}".format(contact_string)

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
        Member.query.delete()
        for mem in members:
            mem_rep = Member(mem['user_id'], mem['name'])
            db.session.add(mem_rep)
            db.session.commit()
        update_globals()
        bot.notify_control("The AnnouncementBot contact list has been successfully updated. {} members total.".format(len(members)))
    except:
        bot.notify_control("WARNING: An error occurred reseeding AnnouncementBot. Please try again.")

    return "OK -- Check control group to make sure request went through..."

if __name__ == '__main__':
    app.run(debug=True)
