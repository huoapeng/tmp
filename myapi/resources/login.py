#coding=utf-8
import datetime
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db
from myapi.model.user import UserModel
from myapi.model.login import LoginModel
from myapi.model.smtp import EmailModel
from myapi.model.tag import UserTagModel
from myapi.model.enum import account_status
from myapi.common.util import valid_email, md5

class Login(Resource):
    def get(self, id):
        login = LoginModel.query.get(id)
        if login:
            return jsonify(login.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('email', type=valid_email, location='json', required=True)
        post_parser.add_argument('password', type=str, location='json')
        args = post_parser.parse_args()

        login = LoginModel.query.filter_by(email=args.email).first()
        if login:
            if login.status == account_status.disable:
                return jsonify(result=False, message='此账号已被冻结！')
        else:
            user = UserModel(args.email)
            db.session.add(user)
            db.session.commit()

            login = LoginModel(args.email, md5(args.password), user.id)
            db.session.add(login)
            db.session.commit()
        
        login = LoginModel.query.filter_by(email=args.email).filter_by(password=md5(args.password)).first()
        if login:
            login.lastLoginDate = datetime.datetime.now()
            db.session.commit()
            return jsonify(result=True, data=login.serialize())
        else:
            return jsonify(result=False, message='用户名或密码错误！')

    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('email', type=valid_email, location='json', required=True)
        post_parser.add_argument('status', type=int, location='json', required=True)
        args = post_parser.parse_args()
        login = LoginModel.query.filter_by(email=args.email).one()
        user = UserModel.query.filter_by(email=args.email).one()
        if login and user:
            login.status = args.status
            user.status = args.status
            db.session.commit()
            return jsonify(login.serialize())
        else:
            return jsonify(result=False, message='未找到此用户')

class ChangePassword(Resource):
    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('email', type=valid_email, location='json', required=True)
        post_parser.add_argument('params', type=str, location='json')
        post_parser.add_argument('password', type=str, location='json')
        post_parser.add_argument('orignalPassword', type=str, location='json')
        args = post_parser.parse_args()
        if args.orignalPassword:
            login = LoginModel.query.filter_by(email=args.email).filter_by(password=md5(args.orignalPassword)).first()
        else:
            login = LoginModel.query.filter_by(email=args.email).first()
            email = EmailModel.query.filter_by(toUser=args.email).filter_by(params=args.params).first()

            if login and email and email.expires < datetime.datetime.now():
                pass
            else:
                return jsonify(result=False, message='请重试')

        if login:
            login.password = md5(args.password)
            db.session.commit()
            return jsonify(login.serialize())
        else:
            return jsonify(result=False, message='未找到此用户')

