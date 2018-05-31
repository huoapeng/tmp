
import datetime
from flask import url_for
from myapi import db
from enum import bid_status, file_type
from myapi.common.file import getUploadFileUrl

class BidModel(db.Model):
    price = db.Column(db.String(100))
    description = db.Column(db.Text)
    timespan = db.Column(db.String(100))
    file = db.Column(db.String(200))
    status = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'), primary_key=True)

    user = db.relationship('UserModel', lazy='joined')
    project = db.relationship('ProjectModel', lazy='joined')

    def __init__(self, price=None, description=None, timespan=None, file=None):
        self.price = price
        self.description = description
        self.timespan = timespan
        self.file = file
        self.status = bid_status.start

    def serialize(self):
        return {
            'price': self.price,
            'description': self.description,
            'timespan': self.timespan,
            'file': getUploadFileUrl(file_type.bidFile, self.user_id, self.file),
            'status': self.status,
            'userid': self.user_id,
            'user': url_for('.user', _external=True, userid=self.user_id),
            'projectid': self.project_id,
            'project': url_for('.project', _external=True, projectid=self.project_id),
        }