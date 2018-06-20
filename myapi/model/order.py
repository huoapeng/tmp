import datetime
from flask import url_for
from myapi import db
from enum import order_status

class OrderModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    publishDate = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    workid = db.Column(db.Integer, db.ForeignKey('work_model.id'))
    buyerid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    sellerid = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, name, price=0):
        self.name = name
        self.price = price
        self.publishDate = datetime.datetime.now()
        self.status = order_status.notPay

    def __repr__(self):
        return '<User %r>' % (self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'publishDate': self.publishDate.isoformat(),
            'status': self.status,    
            'workid': self.workid,
            'buyerid': self.buyerid,
            'sellerid': self.sellerid,        
            'buyer': url_for('.user', _external=True, userid=self.buyerid),
            'seller': url_for('.user', _external=True, userid=self.sellerid)      
        }

