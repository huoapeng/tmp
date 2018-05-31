import datetime
from myapi import db

class EmailModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    params = db.Column(db.Text)
    sendDate = db.Column(db.DateTime)
    expires = db.Column(db.DateTime)

    toUser = db.Column(db.String(200))

    def __init__(self, toUser=None, params=None, expires=None):
        self.toUser = toUser
        self.params = params
        self.sendDate = datetime.datetime.now()
        self.expires = expires

    def serialize(self):
        return {
            # 'noteid': self.id,
            # 'userid': self.owner.id,
            # 'userName': self.owner.nickname,
            # 'userImage': self.owner.getImage(),
            # 'title': self.title,
            # 'publishDate': self.publishDate.isoformat()
        }