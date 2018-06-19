import datetime
from flask import url_for
from myapi import db
from myapi.model.tag import work_tags
from myapi.model.enum import work_status, file_type
from myapi.common.file import getUploadFileUrl


class WorkModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    thumbnail = db.Column(db.String(200))
    image = db.Column(db.String(200))
    file = db.Column(db.String(200))
    description = db.Column(db.Text)
    copyright = db.Column(db.Integer)
    status = db.Column(db.Integer)
    publishDate = db.Column(db.DateTime)
    price = db.Column(db.Integer)

    ownerid = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    tags = db.relationship('WorkTagModel', secondary=work_tags,
                           backref=db.backref('works', lazy='dynamic'))
    pics = db.relationship('WorkPicModel', backref=db.backref(
        'work', lazy='joined'), lazy='dynamic')
    messages = db.relationship('WorkMessageModel', order_by="WorkMessageModel.publishDate",
                               backref=db.backref('work', lazy='joined'), lazy='dynamic')

    def __init__(self, title=None, thumbnail=None, image=None, file=None, description=None, copyright=None, price=0):
        self.title = title
        self.thumbnail = thumbnail
        self.image = image
        self.file = file
        self.description = description
        self.copyright = copyright
        self.status = work_status.normal
        self.publishDate = datetime.datetime.now()
        self.price = price

    def __repr__(self):
        return '<User %r>' % (self.title)

    def serialize(self):
        return {
            'userid': self.ownerid,
            'workid': self.id,
            'title': self.title,
            'thumbnail': getUploadFileUrl(file_type.workThumbnail, self.ownerid, self.thumbnail),
            'image': getUploadFileUrl(file_type.work, self.ownerid, self.image),
            'file': getUploadFileUrl(file_type.workFile, self.ownerid, self.file),
            'description': self.description,
            'copyright': self.copyright,
            'status': self.status,
            'publishDate': self.publishDate.isoformat(),
            'owner': url_for('.user', _external=True, userid=self.ownerid),
            'tags': url_for('.workTags', _external=True, workid=self.id),
            'price': self.price
        }


class WorkPicModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    num = db.Column(db.Integer)

    workid = db.Column(db.Integer, db.ForeignKey('work_model.id'))
    ownerid = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, image, num):
        self.image = image
        self.num = num

    def __repr__(self):
        return '<User %r>' % (self.num)

    def serialize(self):
        return {
            'workid': self.workid,
            'ownerid': self.ownerid,
            'image': getUploadFileUrl(file_type.workPic, self.ownerid, self.image),
            'num': self.num
        }
