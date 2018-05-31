from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.bid import BidModel
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel
from myapi.model.enum import bid_status, project_status

post_parser = reqparse.RequestParser()
post_parser.add_argument('projectid', type=int, location='json', required=True)
post_parser.add_argument('userid', type=int, location='json', required=True)
post_parser.add_argument('price', type=str, location='json')
post_parser.add_argument('description', type=str, location='json')
post_parser.add_argument('timespan', type=str, location='json')
post_parser.add_argument('file', type=str, location='json')

class Bid(Resource):
    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('projectid', type=int, location='args', required=True)
        get_parser.add_argument('userid', type=int, location='args', required=True)
        args = get_parser.parse_args()
        e = BidModel.query.filter_by(user_id=args.userid).filter_by(project_id=args.projectid).first()
        return jsonify(data=e.serialize() if e else '')

    def post(self):
        args = post_parser.parse_args()
        bid = BidModel(args.price, args.description, args.timespan, args.file)

        user = UserModel.query.get(args.userid)
        bid.user = user

        project = ProjectModel.query.get(args.projectid)
        project.bidders.append(bid)

        db.session.commit()
        return jsonify(bid.serialize())

    def put(self):
        args = post_parser.parse_args()
        bid = BidModel.query.filter_by(user_id=args.userid).filter_by(project_id=args.projectid).first_or_404()
        bid.status = bid_status.selectBidder

        project = ProjectModel.query.get(args.projectid)
        project.status = project_status.selectBidder

        user = UserModel.query.get(args.userid)
        user.wonProjects.append(project)

        db.session.commit()
        return jsonify(result='true')

class BidList(Resource):
    def get(self, projectid):
        return jsonify(data=[e.serialize() for e in BidModel.query.filter_by(project_id=projectid)])

class BidCount(Resource):
    def get(self, projectid):
        return jsonify(count=BidModel.query.filter_by(project_id=projectid).count())

