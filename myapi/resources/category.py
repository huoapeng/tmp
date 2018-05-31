from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db
from myapi.model.category import CategoryModel
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel
from myapi.model.enum import category_status

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, location='json')
parser.add_argument('name', type=str, location='json')
parser.add_argument('parentid', type=int, location='json')

class Category(Resource):
    def get(self, cid):
        return jsonify(CategoryModel.query.get(cid).first().serialize())

    def post(self):
        args = parser.parse_args()

        if args.parentid and not CategoryModel.query.get(args.parentid):
            return jsonify(result=False, message='wrong parentid')

        category = CategoryModel(args.name)
        db.session.add(category)
        db.session.commit()

        if args.parentid:
            parent = CategoryModel.query.get(args.parentid)
            category.parent_id = parent.id
            db.session.commit()       
        else:
            category.parent_id = category.id
            db.session.commit()

        return jsonify(category.serialize())

    def put(self):
        args = parser.parse_args()
        category = CategoryModel.query.get(args.id)
        category.name = args.name
        category.parent_id = args.parentid
        db.session.commit()
        return jsonify(category.serialize())

    def delete(self):
        args = parser.parse_args()
        category = CategoryModel.query.get(args.id)
        category.status = category_status.delete
        db.session.commit()
        return jsonify(category.serialize())

class CategoryList(Resource):
    def get(self):
        return jsonify(data=[e.serialize() for e in CategoryModel.query\
            .filter_by(status = category_status.normal)])

class SearchCategorysByName(Resource):
    def get(self, keyword):
        return jsonify(data=[e.serialize() for e in CategoryModel.query\
            .filter_by(status = category_status.normal)\
            .filter(CategoryModel.name.contains(keyword))])

class ProjectCategorys(Resource):
    def get(self, projectid):
        categorys = CategoryModel.query.filter_by(status = category_status.normal)\
            .filter(CategoryModel.projects.any(ProjectModel.id == projectid))
        return jsonify(data=[e.serialize() for e in categorys])

class UserCategorys(Resource):
    def get(self, userid):
        categorys = CategoryModel.query.filter_by(status = category_status.normal)\
            .filter(CategoryModel.users.any(UserModel.id == userid))
        return jsonify(data=[e.serialize() for e in categorys])
