from server import db

class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(50), unique = False)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return '<Name [{}], UID [{}]>'.format(self.name, self.user_id)
