#coding=utf-8
from flask.ext.restful import Resource, reqparse
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

    def post(self):
        print 123
        parser = reqparse.RequestParser()
        parser.add_argument('test', type=str, location='json', required=True)
        args = parser.parse_args()
        print args

        return args

