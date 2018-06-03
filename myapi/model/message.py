import datetime
from myapi import db

# class VersionMessageModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String(1000))
#     publishDate = db.Column(db.DateTime)

#     version_id = db.Column(db.Integer, db.ForeignKey('version_model.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

#     def __init__(self, message):
#         self.message = message
#         self.publishDate = datetime.datetime.now()

#     def __repr__(self):
#         return '<User %r>' % (self.message)


class NoteMessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    publishDate = db.Column(db.DateTime)

    note_id = db.Column(db.Integer, db.ForeignKey('note_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, message):
        self.message = message
        self.publishDate = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.message)

    def serialize(self):
        return {
            'userid': self.owner.id,
            'userName': self.owner.nickname,
            'userImage': self.owner.getImage(),
            'message': self.message,
            'publishDate': self.publishDate
        }

class WorkMessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    publishDate = db.Column(db.DateTime)

    work_id = db.Column(db.Integer, db.ForeignKey('work_model.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, message):
        self.message = message
        self.publishDate = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.message)

    def serialize(self):
        return {
            'buyer_id': self.buyer.id,
            'buyerName': self.buyer.nickname,
            'buyerImage': self.buyer.getImage(),
            'seller_id': self.seller.id,
            'sellerName': self.seller.nickname,
            'sellerImage': self.seller.getImage(),
            'message': self.message,
            'publishDate': self.publishDate
        }