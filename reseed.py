import requests

GROUPME_API = "https://api.groupme.com/v3"
# ACCESS_TOK = "sWNFUhEiTLajKC9R3rnEblOx13o1yc5anbCqswp3"
# APP_CLIENT_ID =


# Do some kind of login
# res = requests.get(GROUPME_API + "/users/me",  params={'token': ACCESS_TOK})
# print res.text


class ContactUpdater(object):

    def __init__(self, redirect_url):
        self.redirect_url = redirect_url

    def authenticate(self):
        print "Please authenticate here:"
        res = self.redirect_url

    def viewGroups(self, access_tok):
        requests.get()

    # def viewGroups(self, ):
