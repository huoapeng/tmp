from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.tag import UserTagModel, WorkTagModel
from myapi.model.user import UserModel
from myapi.model.work import WorkModel
from myapi.model.enum import tag_status
# from sqlalchemy import func

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, location='json')
parser.add_argument('name', type=str, location='json')
parser.add_argument('userid', type=int, location='json')
parser.add_argument('workid', type=int, location='json')
parser.add_argument('status', type=int, location='json')

tag_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'status': fields.Integer
}

class UserTag(Resource):
    @marshal_with(tag_fields)
    def get(self, tagid):
        return UserTagModel.query.get(tagid)

    @marshal_with(tag_fields)
    def post(self):
        args = parser.parse_args()
        tag = UserTagModel.query.filter_by(name = args.name).first()
        if not tag:
            tag = UserTagModel(args.name)
            db.session.add(tag)
            db.session.commit()

        if args.userid:
            user = UserModel.query.get(args.userid)
            user.tags.append(tag)
            db.session.commit()
        return tag

    def put(self):
        args = parser.parse_args()
        tag = UserTagModel.query.get(args.id)
        tag.status = args.status
        db.session.commit()
        return jsonify(result='True')

    def delete(self):
        args = parser.parse_args()
        tag = UserTagModel.query.get(args.id)
        user = UserModel.query.get(args.userid)
        user.tags.remove(tag)
        db.session.commit()
        return jsonify(result='True')

class UserTags(Resource):
    @marshal_with(tag_fields)
    def get(self, userid):
        tags = UserTagModel.query\
            .filter_by(status = tag_status.normal)\
            .filter(UserTagModel.users.any(UserModel.id == userid)).all()
        return tags

class UserTagList(Resource):
    def get(self, page):
        # tags = db.session.query(UserTagModel.name, func.count(UserTagModel.name)).\
        #     group_by(UserTagModel.name).order_by(func.count(UserTagModel.name).desc()).limit(limit)
        # return jsonify(data=[e for e in tags])
        tags = UserTagModel.query.filter_by(status = tag_status.normal)\
            .paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = tags.total,
            pages = tags.pages,
            page = tags.page,
            per_page = tags.per_page,
            has_next = tags.has_next,
            has_prev = tags.has_prev,
            next_num = tags.next_num,
            prev_num = tags.prev_num,
            data=[e.serialize() for e in tags.items])
 

class SearchUserTagsByName(Resource):
    @marshal_with(tag_fields)
    def get(self, keyword):
        return UserTagModel.query.filter(UserTagModel.name.contains(keyword))\
            .filter_by(status = tag_status.normal).all()

class WorkTag(Resource):
    @marshal_with(tag_fields)
    def get(self, tagid):
        return WorkTagModel.query.get(tagid)

    @marshal_with(tag_fields)
    def post(self):
        args = parser.parse_args()
        tag = WorkTagModel.query.filter_by(name = args.name).first()
        if not tag:
            tag = WorkTagModel(args.name)
            db.session.add(tag)
            db.session.commit()
        return tag

    def delete(self):
        args = parser.parse_args()
        tag = WorkTagModel.query.get(args.id)
        work = WorkTagModel.query.get(args.workid)
        work.tags.remove(tag)
        db.session.commit()
        return jsonify(result='true')

class WorkTags(Resource):
    @marshal_with(tag_fields)
    def get(self, workid):
        work = WorkModel.query.get(workid)
        return work.tags

class SearchWorkTagsByName(Resource):
    @marshal_with(tag_fields)
    def get(self, keyword):
        return WorkTagModel.query.filter(WorkTagModel.name.contains(keyword)).all()