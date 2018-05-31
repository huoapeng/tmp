import datetime
from flask import url_for
from myapi import db
from myapi.common.file import getUploadFileUrl
from myapi.model.enum import file_type

class RecommendTypeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    items = db.relationship('RecommendItemModel', order_by="RecommendItemModel.orderid",
        backref=db.backref('type', lazy='joined'), lazy='dynamic')
    
    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': url_for('.recommendItem', _external=True, typeid=self.id)
        }

class RecommendItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    url = db.Column(db.String(200))
    orderid = db.Column(db.Integer)

    typeid = db.Column(db.Integer, db.ForeignKey('recommend_type_model.id'))

    def __init__(self, title, description, image, url, orderid):
        self.title = title
        self.description = description
        self.image = image
        self.url = url
        self.orderid = orderid

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': getUploadFileUrl(file_type.recommend, self.typeid, self.image),
            'imageName': self.image,
            'url':self.url,
            'orderid': self.orderid
        }
