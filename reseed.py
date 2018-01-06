import requests, json

GROUPME_API = "https://api.groupme.com/v3"

class ContactUpdater(object):

    def __init__(self, redirect_url):
        self.redirect_url = redirect_url

    def authenticate(self):
        return self.redirect_url

    def getGroups(self, auth_tok):
        res = requests.get(GROUPME_API + "/groups", params = {"token":auth_tok})
        data = res.json()["response"]
        data = [{
            "name": group["name"],
            "members":
                [{"name": mem["nickname"], "user_id": mem["user_id"]} for mem in group["members"]]
        } for group in data]
    
        return data
