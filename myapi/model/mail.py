import datetime
from enum import mail_status

class MailModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    status = db.Column(db.Integer)
    publishDate = db.Column(db.DateTime)

    receiver_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.status = mail_status.unread
        self.publishDate = datetime.datetime.now()

    def serialize(self):
        return {
            'receiverID': self.receiver_id,
            'title': self.title,
            'content': self.content,
            'status': self.status,
            'publishDate': self.publishDate
        }

class MailTemplateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    description = db.Column(db.Text)

    trigger_id = db.Column(db.Integer, db.ForeignKey('mail_trigger_model.id'))

    def __init__(self, title, content, description):
        self.title = title
        self.content = content
        self.description = description

    def serialize(self):
        return {
            'title': self.title,
            'content': self.content,
            'description': self.description
        }

class MailTriggerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))

    templates = db.relationship('MailTemplateModel', backref=db.backref('trigger', lazy='joined'), lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            'name': self.name
        }





