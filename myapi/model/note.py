import datetime
from myapi import db
from enum import note_status

class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    publishDate = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    messages = db.relationship('NoteMessageModel', order_by="NoteMessageModel.publishDate",
        backref=db.backref('note', lazy='joined'), lazy='dynamic')

    def __init__(self, title):
        self.title = title
        self.publishDate = datetime.datetime.now()
        self.status = note_status.normal

    def __repr__(self):
        return '<User %r>' % (self.title)

    def serialize(self):
        return {
            'noteid': self.id,
            'userid': self.user_id,
            'userName': self.owner.nickname,
            'userImage': self.owner.getImage(),
            'title': self.title,
            'publishDate': self.publishDate.isoformat()
        }