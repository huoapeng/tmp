import datetime
from flask import url_for
from myapi import db
from enum import project_status
from category import project_categorys

class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    timespan = db.Column(db.String(200))
    requirements = db.Column(db.Text)
    bonus = db.Column(db.Integer)
    description = db.Column(db.Text)
    publishDate = db.Column(db.DateTime)
    bidderQualifiRequire = db.Column(db.String(100))
    bidderLocationRequire = db.Column(db.String(100))
    status = db.Column(db.Integer)
    receipt = db.Column(db.Boolean)
    receiptDes = db.Column(db.String(500))

    ownerid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    winnerid = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    categorys = db.relationship('CategoryModel', secondary=project_categorys, 
        backref=db.backref('projects', lazy='dynamic'))
    versions = db.relationship('VersionModel', backref=db.backref('project', lazy='joined'), lazy='dynamic')
    notes = db.relationship('NoteModel', backref=db.backref('project', lazy='joined'), lazy='dynamic')
    bidders = db.relationship('BidModel', lazy='dynamic')

    def __init__(self, name, timespan=None, requirements=None, bonus=0, description=None, 
        bidderQualifiRequire=None, bidderLocationRequire=None, receipt=False, receiptDes=None):
        self.name = name
        self.timespan = timespan
        self.requirements = requirements
        self.bonus = bonus
        self.description = description
        self.publishDate = datetime.datetime.now()
        self.bidderQualifiRequire = bidderQualifiRequire
        self.bidderLocationRequire = bidderLocationRequire
        self.status = project_status.disable
        self.receipt = receipt
        self.receiptDes = receiptDes

    def __repr__(self):
        return '<User %r>' % (self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'timespan': self.timespan,
            'requirements': self.requirements,
            'bonus': self.bonus,
            'description': self.description,
            'publishDate': self.publishDate.isoformat(),
            'bidderQualifiRequire': self.bidderQualifiRequire,
            'bidderLocationRequire': self.bidderLocationRequire,
            'status': self.status,
            'receipt': self.receipt,
            'receiptDes': self.receiptDes,
            'owner': url_for('.user', _external=True, userid=self.ownerid),
            'winner': url_for('.user', _external=True, userid=self.winnerid) if self.winnerid else '',
            'versions': url_for('.projectVersions', _external=True, projectid=self.id),
            'notes': url_for('.projectNotes', _external=True, projectid=self.id),
            'bids': url_for('.projectBids', _external=True, projectid=self.id),
            'bidCount': url_for('.projectCount', _external=True, projectid=self.id),
            'categorys': url_for('.projectCategorys', _external=True, projectid=self.id)
        }

