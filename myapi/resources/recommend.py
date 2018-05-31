from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.recommend import RecommendTypeModel, RecommendItemModel

post_parser = reqparse.RequestParser()
post_parser.add_argument('typeid', type=int, location='json')
post_parser.add_argument('itemid', type=int, location='json')
post_parser.add_argument('targetitemid', type=int, location='json')
post_parser.add_argument('name', type=str, location='json')
post_parser.add_argument('title', type=str, location='json')
post_parser.add_argument('description', type=str, location='json')
post_parser.add_argument('image', type=str, location='json')
post_parser.add_argument('url', type=str, location='json')
post_parser.add_argument('orderid', type=int, location='json')

class RecommendType(Resource):
    def get(self, id):
        category = RecommendTypeModel.query.get(id)
        return jsonify(data=category.serialize()) if category else jsonify(data='')
    
    def post(self):
        args = post_parser.parse_args()

        category = RecommendTypeModel(args.name)
        db.session.add(category)
        db.session.commit()

        return jsonify(data=category.serialize())

    def put(self):
        args = post_parser.parse_args()
        category = RecommendTypeModel.query.get(args.typeid)
        category.name = args.name
        db.session.commit()
        return jsonify(data=category.serialize())

    def delete(self):
        args = post_parser.parse_args()
        category = RecommendTypeModel.query.get(args.typeid)
        for item in category.items:
            db.session.delete(item)
        db.session.delete(category)
        db.session.commit()
        return jsonify(result='true')

class RecommendTypeList(Resource):
    def get(self):
        categorys = RecommendTypeModel.query.all()
        return jsonify(data=[category.serialize() for category in categorys])

class RecommendItem(Resource):
    def get(self, id):
        item = RecommendItemModel.query.get(id)
        return jsonify(data=item.serialize()) if item else jsonify(data='')
    
    def post(self):
        args = post_parser.parse_args()
        item = RecommendItemModel(args.title, args.description, args.image, args.url, args.orderid)
        db.session.add(item)

        category = RecommendTypeModel.query.get(args.typeid)
        category.items.append(item)
        db.session.commit()
        return jsonify(data=item.serialize())

    def put(self):
        args = post_parser.parse_args()
        item = RecommendItemModel.query.get(args.itemid)
        item.title = args.title
        item.description = args.description
        item.image = args.image
        item.url = args.url
        item.orderid = args.orderid

        # target = RecommendItemModel.query.get(args.targetitemid)
        # item.orderid = target.orderid
        # target.orderid = orderid

        db.session.commit()
        return jsonify(data=item.serialize())

    def delete(self):
        args = post_parser.parse_args()
        item = RecommendItemModel.query.get(args.itemid)

        db.session.delete(item)
        db.session.commit()
        return jsonify(result='true')

class RecommendItemList(Resource):
    def get(self, typeid):
        category = RecommendTypeModel.query.get(typeid)
        if category and category.items:
            return jsonify(data=[item.serialize() for item in category.items])
        else:
            return jsonify(data='')

