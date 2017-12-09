GROUPME_API = "https://api.groupme.com/v3/"
ACCESS_TOK = "sWNFUhEiTLajKC9R3rnEblOx13o1yc5anbCqswp3"

class AnnouncementBot(object):

	def __init__(self, token, bot_id, contacts, message_filter=None, base_guid='announcement-bot'):
		self.token = token
		self.bot_id = bot_id
		self.contacts = contacts
		self.base_guid = base_guid
		self.message_filter = message_filter

	def send_announcement(self, message):
		if not self.message_filter(message):
			for contact in self.contacts:
				json = {
					'message': {
						'source_guid': '{}-{}-{}'.format(self.base_guid, contact, time.time()),
						'recipient_id': contact,
						'text': 'From {}:\n{}'.format(message['name'], message['text'])
					}
				}

				requests.post(GROUPME_API + '/direct_messages', params={'token': self.token}, json=json)

			# json = {
			# 	'bot_id': self.bot_id,
			# 	'text': 'Message sent to {} recipients.'.format(len(self.contacts))
			# }
			# requests.post(GROUPME_API + '/bots/post', params={'token': self.token}, json=json)
