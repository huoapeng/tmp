import datetime
from flask import url_for
from myapi import db
from myapi.common.file import getUploadFileUrl
from myapi.model.enum import file_type

class ApprovalModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    authenticationType = db.Column(db.Integer)
    authenticationID = db.Column(db.Integer)
    approvalStatus = db.Column(db.Integer)
    approvalDate = db.Column(db.DateTime)
    userid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    adminid = db.Column(db.Integer)
    description = db.Column(db.Text)

    def __init__(self, authenticationType, authenticationID, approvalStatus, userid, adminid, description):
        self.authenticationType = authenticationType
        self.authenticationID = authenticationID
        self.approvalStatus = approvalStatus
        self.approvalDate = datetime.datetime.now()
        self.userid = userid
        self.adminid = adminid
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'type': self.authenticationType,
            'authenID': self.authenticationID,
            'approvalStatus': self.approvalStatus,
            'approvalDate': self.approvalDate,
            'userid': self.userid,
            'user': url_for('.user', _external=True, userid=self.userid),
            'adminid': self.adminid,
            'admin': url_for('.user', _external=True, userid=self.adminid),
            'description': self.description
        }

class PrivateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200))
    authenticateDate = db.Column(db.DateTime)
    identityID = db.Column(db.String(50), nullable=False)
    identityFrontImage = db.Column(db.String(100), nullable=False)
    identityBackImage = db.Column(db.String(100), nullable=False)

    userid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    approvalStatus = db.Column(db.Integer)

    def __init__(self, name, identityID, identityFrontImage, identityBackImage):
        self.name = name
        self.authenticateDate = datetime.datetime.now()
        self.identityID = identityID
        self.identityFrontImage = identityFrontImage
        self.identityBackImage = identityBackImage

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'authenticateDate': self.authenticateDate,
            'identityID': self.identityID,
            'identityFrontImage': getUploadFileUrl(file_type.privateFront, self.userid,  self.identityFrontImage),
            'identityBackImage': getUploadFileUrl(file_type.privateBack, self.userid, self.identityBackImage),
            'userid': self.userid,
            'status': self.approvalStatus
        }

class CompanyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200))
    authenticateDate = db.Column(db.DateTime)
    businessScope = db.Column(db.Text)
    licenseID = db.Column(db.String(500))
    licenseImage = db.Column(db.String(500))
    contactImage = db.Column(db.String(500))

    userid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    approvalStatus = db.Column(db.Integer)

    def __init__(self, name, businessScope, licenseID, licenseImage, contactImage):
        self.name = name
        self.authenticateDate = datetime.datetime.now()
        self.businessScope = businessScope
        self.licenseID = licenseID
        self.licenseImage = licenseImage
        self.contactImage = contactImage

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'authenticateDate': self.authenticateDate,
            'businessScope': self.businessScope,
            'licenseID':self.licenseID,
            'licenseImage': getUploadFileUrl(file_type.companyLience, self.userid, self.licenseImage),
            'contactImage': getUploadFileUrl(file_type.companyContactCard, self.userid, self.contactImage),
            'userid': self.userid,
            'status': self.approvalStatus
        }

class BankModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200))
    authenticateDate = db.Column(db.DateTime)
    bankAccount = db.Column(db.String(100))
    bankName = db.Column(db.String(500))
    bankLocation = db.Column(db.String(200))
    checkCode = db.Column(db.Integer)

    userid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    approvalStatus = db.Column(db.Integer)

    def __init__(self, name, bankAccount, bankName, bankLocation):
        self.name = name
        self.authenticateDate = datetime.datetime.now()
        self.bankAccount = bankAccount
        self.bankName = bankName
        self.bankLocation = bankLocation

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'authenticateDate': self.authenticateDate,
            'bankAccount': self.bankAccount,
            'bankName': self.bankName,
            'bankLocation': self.bankLocation,
            'userid': self.userid,
            'status': self.approvalStatus,
            'checkCode': self.checkCode
        }

class ManualModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    location = db.Column(db.String(100))
    authenticateDate = db.Column(db.DateTime)

    userid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    approvalStatus = db.Column(db.Integer)

    def __init__(self, name, phone, location):
        self.name = name
        self.phone = phone
        self.location = location
        self.authenticateDate = datetime.datetime.now()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'authenticateDate': self.authenticateDate,
            'phone': self.phone,
            'location': self.location,
            'userid': self.userid,
            'status': self.approvalStatus
        }
        