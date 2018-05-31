import datetime
from flask import url_for
from myapi import db
from enum import account_status

class LoginModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    lastLoginDate = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    user_id = db.Column(db.Integer, unique=True)

    def __init__(self, email, password, userid):
        self.email = email
        self.password = password
        self.lastLoginDate = datetime.datetime.now()
        self.status = account_status.disable
        self.user_id = userid

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'lastLoginDate': self.lastLoginDate,
            'status': self.status,
            'user': url_for('.user', _external=True, userid=self.user_id)
        }


