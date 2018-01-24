import requests, json, time

GROUPME_API = "https://api.groupme.com/v3"
BOT_API = "https://api.groupme.com/v3/bots/post"

class AnnouncementBot(object):

    def __init__(self, token, bot_id, contacts, base_guid='announcement-bot'):
        self.token = token # User token of account used to send annoucements. NOTE: NOT A GMe bot!
        self.bot_id = bot_id # Bot_id of bot listening in control group
        self.contacts = contacts
        self.base_guid = base_guid

    """Method notifies the AnnouncementBot control group with provided [message]."""
    def notify_control(self, message):
        msg = {'bot_id': self.bot_id,'text': message}
        requests.post(BOT_API, params={'token': self.token}, json = msg)

    """Method notifies each contact in [contacts] of the provided [message] via
    a GroupMe direct message. Control group is notified with result."""
    def send_announcement(self, message):

        ok_results = err_results = 0

        for idx, contact in enumerate(self.contacts):

            # Notifying contacts
            msg = {
            	'message': {
            		'source_guid': '{}-{}-{}'.format(self.base_guid, contact, time.time()),
            		'recipient_id': contact,
            		'text': 'From {}:\n{}'.format(message['name'], message['text'])
            	}
            }

            res = requests.post(GROUPME_API + '/direct_messages', params={'token': self.token}, json=msg)

            if res.status_code == 201:
                ok_results += 1
            else:
                err_results += 1
                print res.text

            # Some jank code to get around rate limit...
            time.sleep(3)
            if (idx + 1) % 20 == 0:
                self.notify_control("Attempted to deliver to {} contacts out of {} total. {} errors so far.".format(idx+1, len(self.contacts), err_results))

        # Sending report to control group
        report = "Message succesfully sent to {} recipients. ".format(ok_results)

        if err_results:
            report += "WARNING {} errors. Your message might not have been delivered to all contacts.".format(err_results)
        else:
            report += "No errors."

        self.notify_control(report)
