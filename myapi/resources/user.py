#coding=utf-8
import datetime
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.user import UserModel
from myapi.model.smtp import EmailModel
from myapi.model.tag import UserTagModel
from myapi.model.category import CategoryModel
from myapi.model.enum import account_status
from myapi.common.util import valid_email, md5

class User(Resource):
    def get(self, userid):
        user = UserModel.query.get(userid)
        if user:
            return jsonify(user.serialize())
        else:
            return jsonify(result=False, message='未找到此用户')

    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('id', type=int, location='json', required=True)
        post_parser.add_argument('nickname', type=str, location='json')
        post_parser.add_argument('phone', type=str, location='json')
        post_parser.add_argument('location', type=str, location='json')
        post_parser.add_argument('description', type=str, location='json')  
        post_parser.add_argument('defaultImage', type=str, location='json')
        post_parser.add_argument('cids', type=str, location='json')
        post_parser.add_argument('status', type=int, location='json')      
        args = post_parser.parse_args()
        user = UserModel.query.get(args.id)
        if user:
            user.nickname = args.nickname
            user.phone = args.phone
            user.location = args.location
            user.description = args.description
            user.defaultImage = args.defaultImage
            user.status = args.status
            if args.cids:
                for c in user.categorys:
                    user.categorys.remove(c)
                for id in args.cids.split(','):
                    category = CategoryModel.query.get(id)
                    user.categorys.append(category)
            db.session.commit()
            return jsonify(user.serialize())
        else:
            return jsonify(result='未找到此用户')

from sqlalchemy import or_
class GetUserList(Resource):
    def get(self, page):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('all', type=int, location='args', choices=range(2), default=0)
        get_parser.add_argument('cid', type=int, location='args', default=0)
        get_parser.add_argument('keyword', type=str, location='args')
        get_parser.add_argument('tag', type=str, location='args')
        get_parser.add_argument('authentype', type=int, location='args', default=0)
        args = get_parser.parse_args()

        users = UserModel.query
        if args.cid:
            users = users.filter( \
                or_( \
                    UserModel.categorys.any(CategoryModel.id == args.cid), \
                    UserModel.categorys.any(CategoryModel.parent_id == args.cid), \
                    UserModel.categorys.any(CategoryModel.parent.has(CategoryModel.parent_id == args.cid))
                    ) \
                )

        if not args.all:
            users = users.filter_by(status = account_status.normal)

        if args.tag:
            users = users.filter(UserModel.tags.any(UserTagModel.name == args.tag))

        if args.keyword:
            users = users.filter(UserModel.nickname.contains(args.keyword))

        if args.authentype:
            users = users.filter(UserModel.authenticationType.op('&')(args.authentype) == args.authentype)

        users = users.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = users.total,
            pages = users.pages,
            page = users.page,
            per_page = users.per_page,
            has_next = users.has_next,
            has_prev = users.has_prev,
            next_num = users.next_num,
            prev_num = users.prev_num,
            data=[e.serialize() for e in users.items])

