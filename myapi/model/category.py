from myapi import db
from enum import category_status

user_categorys = db.Table('user_categorys',
    db.Column('category_id', db.Integer, db.ForeignKey('category_model.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user_model.id'), primary_key=True)
)

project_categorys = db.Table('project_categorys',
    db.Column('category_id', db.Integer, db.ForeignKey('category_model.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project_model.id'), primary_key=True)
)

class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.Integer)

    parent_id = db.Column(db.Integer, db.ForeignKey('category_model.id'))

    parent = db.relationship('CategoryModel', remote_side=[id], 
        backref=db.backref('kids', lazy='dynamic'), lazy='joined')

    def __init__(self, name):
    	self.name = name
        self.status = category_status.normal

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'parentid': self.parent_id,
            'status': self.status
        }
