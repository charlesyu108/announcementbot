from flask import Flask, request, redirect, url_for, render_template, make_response
import requests, json, time, csv, os
from bot import AnnouncementBot
from reseed import ContactUpdater
from load import load_env_var
from auth import requires_auth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

GROUPME_API = "https://api.groupme.com/v3"
BOT_ID = load_env_var('BOT_ID')
ACCESS_TOK = load_env_var('ACCESS_TOK')
APP_REDIRECT = load_env_var('APP_REDIRECT')
DB_URL = load_env_var("DATABASE_URL")
ADMIN_USER = load_env_var("ADMIN_USER")
ADMIN_PASS = load_env_var("ADMIN_PASS")

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
site_credentials = { 'username': ADMIN_USER, 'password': ADMIN_PASS }

def update_globals():
    global contacts
    contacts = Member.query.all()
    contact_ids = [c.user_id for c in contacts]
    global bot
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
    return render_template("contacts.html", members = contacts, editable = False)

@app.route("/contacts/edit", methods = ["GET"])
@requires_auth(creds = site_credentials )
def editContacts():
    return render_template("contacts.html", members = contacts, editable = True)

@app.route("/contacts/add", methods = ["POST"])
def addContact():
    try:
        name = request.form["name"]
        u_id = request.form["user_id"]
        member = Member(u_id, name)

        int(u_id) #testing valid u_id

        exists = db.session.query(Member).filter(Member.user_id == u_id).first()
        if exists:
            msg = "Error. User ID is already in contacts."
            return render_template("contacts.html", members = contacts, err_msg = msg, editable = True)

        db.session.add(member)
        db.session.commit()
        update_globals()
        msg = "Successfully added user {}!".format(name)
        return render_template("contacts.html", members = contacts, msg = msg, editable = True)

    except Exception as e:
        print e
        update_globals()
        msg = "Something went wrong... Please try again."
        return render_template("contacts.html", members = contacts, err_msg = msg, editable = True)

@app.route("/contacts/delete", methods = ["POST"])
def deleteContact():
    u_id = request.form["user_id"]

    try:
        member = db.session.query(Member).filter(Member.user_id == u_id).first()
        db.session.delete(member)
        db.session.commit()
        update_globals()
        msg = "Successfully deleted user with ID {}!".format(u_id)
        return render_template("contacts.html", members = contacts, msg = msg, editable = True)

    except Exception as e:
        print e
        update_globals()
        msg = "Something went wrong... Please try again."
        return render_template("contacts.html", members = contacts, err_msg = msg, editable = True)

@app.route("/listen", methods = ["POST"])
def onMessage():
    message = json.loads(request.data)
    if message['sender_type'] != 'bot' and not message['system']: #ignores system and bot notifications
        bot.send_announcement(message)
    return "OK"

@app.route("/reseed", methods = ["GET"])
@requires_auth(creds = site_credentials )
def auth_reseed():
    return redirect(updater.authenticateUser())

@app.route("/reseed/authenticate_result", methods = ["GET"])
def auth_approved():
    u_auth_tok = request.args.get("access_token")
    if not u_auth_tok:
        return redirect(url_for('auth_reseed'))
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
    except Exception as e:
        print e
        bot.notify_control("WARNING: An error occurred reseeding AnnouncementBot. Please try again.")
    return redirect(url_for('viewContacts'))

if __name__ == '__main__':
    app.run(debug=True)
