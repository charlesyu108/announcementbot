import requests, json

GROUPME_API = "https://api.groupme.com/v3"

class ContactUpdater(object):
    
    """Init function. redirect_url should be the one provided by GroupMe upon
    registering your GroupMe application."""
    def __init__(self, redirect_url):
        self.redirect_url = redirect_url

    """Returns the redirect_url."""
    def authenticateUser(self):
        return self.redirect_url

    """Retrieves the group data for an authenticated user with auth_tok."""
    def getGroups(self, auth_tok):
        res = requests.get(GROUPME_API + "/groups", params = {"token":auth_tok})
        data = res.json()["response"]
        data = [
            {
                "name": group["name"],
                "member_json": json.dumps(
                    [ {"user_id": mem["user_id"], "name": mem["nickname"] }
                    for mem in group["members"] ]),
                "members": [mem["nickname"] for mem in group["members"]]
            }
            for group in data
        ]
        return data
