import datetime, random
from flask import url_for
from myapi import db, app
from enum import account_status, file_type, authentication_type
from tag import user_tags
from category import user_categorys
from myapi.common.file import getUploadFileUrl, getDefaultImageUrl

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(50))
    location = db.Column(db.String(200))
    imageLarge = db.Column(db.String(200))
    imageMedium = db.Column(db.String(200))
    imageSmall = db.Column(db.String(200))
    defaultImage = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.Integer)
    authenticationType = db.Column(db.Integer)
    registDate = db.Column(db.DateTime)

    categorys = db.relationship('CategoryModel', secondary=user_categorys, lazy='dynamic',
        backref=db.backref('users', lazy='dynamic'))

    tags = db.relationship('UserTagModel', secondary=user_tags, backref=db.backref('users', lazy='dynamic'))
    versions = db.relationship('VersionModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    notes = db.relationship('NoteModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    notemessages = db.relationship('NoteMessageModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    works = db.relationship('WorkModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    workpics = db.relationship('WorkPicModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    senderMessages = db.relationship('WorkMessageModel', foreign_keys='WorkMessageModel.sender_id',
        backref=db.backref('sender', lazy='joined'), lazy='dynamic')
    buyerMessages = db.relationship('WorkMessageModel', foreign_keys='WorkMessageModel.buyer_id',
        backref=db.backref('buyer', lazy='joined'), lazy='dynamic')
    sellerMessages = db.relationship('WorkMessageModel', foreign_keys='WorkMessageModel.seller_id',
        backref=db.backref('seller', lazy='joined'), lazy='dynamic')

    boughtOrders = db.relationship('OrderModel', primaryjoin='UserModel.id==OrderModel.buyerid', 
        backref=db.backref('buyer', lazy='joined'), lazy='dynamic')
    soldOrders = db.relationship('OrderModel', primaryjoin='UserModel.id==OrderModel.sellerid', 
        backref=db.backref('seller', lazy='joined'), lazy='dynamic')

    publishedProjects = db.relationship('ProjectModel', primaryjoin='UserModel.id==ProjectModel.ownerid', 
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    wonProjects = db.relationship('ProjectModel', primaryjoin='UserModel.id==ProjectModel.winnerid', 
        backref=db.backref('winner', lazy='joined'), lazy='dynamic')
    bidProjects = db.relationship('BidModel', lazy='dynamic')

    authentications = db.relationship('ApprovalModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    privateAuthenHistory = db.relationship('PrivateModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    companyAuthenHistory = db.relationship('CompanyModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    bankAuthenHistory = db.relationship('BankModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    manualAuthenHistory = db.relationship('ManualModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    def __init__(self, email, nickname=None, phone=None, location=None, description=None):
        if nickname:
            self.nickname = nickname
        else:
            self.nickname = email[:email.find(r'@')]
        self.defaultImage = '{}.jpg'.format(random.randint(1, app.config['DEFAULT_IMAGE_COUNT']))
        self.email = email
        self.phone = phone
        self.location = location
        self.description = description
        self.registDate = datetime.datetime.now()
        self.authenticationType = authentication_type.none

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def serialize(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'imageLarge': self.getImage(file_type.profileLarge),
            'imageMedium': self.getImage(file_type.profileMedium),
            'imageSmall': self.getImage(file_type.profileSmall),
            'description': self.description,
            'defaultImage': self.defaultImage,
            'status': self.status,
            'authenticationType': self.authenticationType,
            'registDate': self.registDate.isoformat(),
            'tags': url_for('.userTags', _external=True, userid=self.id),
            'works': url_for('.userWorks', _external=True, userid=self.id, page=1),
            'publishedProjects': url_for('.userPublishedProjects', _external=True, userid=self.id, page=1),
            'participateProjects': url_for('.userParticipateProjects', _external=True, userid=self.id, page=1),
            'privateAuthentication': url_for('.userAuthen', _external=True, userid=self.id, type=1),
            'companyAuthentication': url_for('.userAuthen', _external=True, userid=self.id, type=2),
            'bankAuthentication': url_for('.userAuthen', _external=True, userid=self.id, type=4),
            'manualAuthentication': url_for('.userAuthen', _external=True, userid=self.id, type=8),
            'categorys': url_for('.userCategorys', _external=True, userid=self.id)
        }

    def getImage(self, imageType=file_type.profileSmall):
        if self.imageLarge and imageType == file_type.profileLarge:
            return getUploadFileUrl(imageType, self.id, self.imageLarge)
        elif self.imageMedium and imageType == file_type.profileMedium:
            return getUploadFileUrl(imageType, self.id, self.imageMedium)
        elif self.imageSmall and imageType == file_type.profileSmall:
            return getUploadFileUrl(imageType, self.id, self.imageSmall)
        else:
            return getDefaultImageUrl(self.defaultImage)


