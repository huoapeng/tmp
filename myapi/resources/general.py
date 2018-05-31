#coding=utf-8
from flask.ext.restful import Resource
from myapi import db

class general(Resource):
    def get(self, method = None):
        if method == 'create_all':
            db.create_all()
        elif method == 'drop_all':
            db.drop_all()
        else:
            return 'hello world! this is a new world!'
        return {'result':'true'}

