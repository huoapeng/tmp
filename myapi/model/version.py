import datetime
from flask import url_for
from myapi import db
from enum import version_status
from myapi.common.file import getUploadFileUrl
from myapi.model.enum import file_type

class VersionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(500))
    image = db.Column(db.String(500))
    title = db.Column(db.String(500))
    description = db.Column(db.Text)
    publishDate = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, title, description, image):
        self.title = title
        self.description = description
        self.image = image
        self.publishDate = datetime.datetime.now()
        self.status = version_status.normal

    def __repr__(self):
        return '<User %r>' % (self.title)

    def serialize(self):
        return {
            'id': self.id,
            'image': getUploadFileUrl(file_type.version, self.user_id, self.image),
            'title': self.title,
            'description': self.description,
            'publishDate': self.publishDate,
            'status': self.status,
            'userid': self.user_id,
            'projectid': self.project_id
        }