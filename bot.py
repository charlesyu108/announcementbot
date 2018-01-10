import requests, json, time

GROUPME_API = "https://api.groupme.com/v3"
BOT_API = "https://api.groupme.com/v3/bots/post"

class AnnouncementBot(object):

    def __init__(self, token, bot_id, contacts, base_guid='announcement-bot'):
        self.token = token
        self.bot_id = bot_id
        self.contacts = contacts
        self.base_guid = base_guid

    def notify_control(self, message):
        msg = {'bot_id': self.bot_id,'text': message}
        requests.post(BOT_API, params={'token': self.token}, json = msg)


    def send_announcement(self, message):

        ok_results = err_results = 0

        for contact in self.contacts:

            # Notifying contacts
            msg = {
            	'message': {
            		'source_guid': '{}-{}-{}'.format(self.base_guid, contact, time.time()),
            		'recipient_id': contact,
            		'text': 'From {}:\n{}'.format(message['name'], message['text'])
            	}
            }

            res = requests.post(GROUPME_API + '/direct_messages', params={'token': self.token}, json=msg)

            if res.status_code == 201: ok_results += 1
            else: err_results += 1

        # Sending report to control group
        report = "Message succesfully sent to {} recipients. ".format(ok_results)

        if err_results:
            report += "WARNING {} errors. Your message might not have been delivered to all contacts.".format(err_results)
        else:
            report += "No errors."

        self.notify_control(report)
