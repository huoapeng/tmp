#coding=utf-8
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.category import CategoryModel
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel
from myapi.model.bid import BidModel
from myapi.model.enum import project_status, bid_status

class Project(Resource):
    def get(self, projectid):
        return ProjectModel.query.get(projectid).serialize()

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('timespan', type=str, location='json')
        post_parser.add_argument('requirements', type=str, location='json')
        post_parser.add_argument('bonus', type=int, location='json')
        post_parser.add_argument('description', type=str, location='json')
        post_parser.add_argument('bidderQualifiRequire', type=str, location='json')
        post_parser.add_argument('bidderLocationRequire', type=str, location='json')
        post_parser.add_argument('receipt', type=bool , location='json')
        post_parser.add_argument('receiptDescription', type=str, location='json')
        post_parser.add_argument('userid', type=int, location='json', required=True)
        post_parser.add_argument('cids', type=str, location='json', required=True)
        args = post_parser.parse_args()

        project = ProjectModel(args.name, 
            args.timespan,
            args.requirements,
            args.bonus,
            args.description,
            args.bidderQualifiRequire,
            args.bidderLocationRequire,
            args.receipt,
            args.receiptDescription)

        for id in args.cids.split(','):
            category = CategoryModel.query.get(id)
            project.categorys.append(category)

        db.session.add(project)

        user = UserModel.query.get(args.userid)
        user.publishedProjects.append(project)
        db.session.commit()
        return project.serialize()

    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('id', type=int, location='json', required=True)
        post_parser.add_argument('status', type=int, location='json', required=True)
        args = post_parser.parse_args()
        project = ProjectModel.query.get(args.id)
        project.status = args.status
        db.session.commit()
        return project.serialize()

class ProjectOneStep(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('buyerid', type=int, location='json', required=True)
        post_parser.add_argument('sellerid', type=int, location='json', required=True)
        post_parser.add_argument('cids', type=str, location='json', required=True)
        args = post_parser.parse_args()

        project = ProjectModel(args.name)
        project.status = project_status.selectBidder

        for id in args.cids.split(','):
            category = CategoryModel.query.get(id)
            project.categorys.append(category)

        db.session.add(project)

        buyer = UserModel.query.get(args.buyerid)
        buyer.publishedProjects.append(project)

        seller = UserModel.query.get(args.sellerid)
        seller.wonProjects.append(project)

        bid = BidModel()
        bid.user = seller
        bid.status = bid_status.selectBidder

        #project = ProjectModel.query.get(args.projectid)
        project.bidders.append(bid)

        db.session.commit()

        return project.serialize()


class UserPublishedProjects(Resource):
    def get(self, page):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=int, location='args', required=True)
        parser.add_argument('status', type=int, location='args', default=0)
        args = parser.parse_args()
        projects = UserModel.query.get(args.userid).publishedProjects

        if args.status:
            projects = projects.filter_by(status = args.status)

        projects = projects.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = projects.total,
            pages = projects.pages,
            page = projects.page,
            per_page = projects.per_page,
            has_next = projects.has_next,
            has_prev = projects.has_prev,
            next_num = projects.next_num,
            prev_num = projects.prev_num,
            data=[e.serialize() for e in projects.items])

class UserParticipateProjects(Resource):
    def get(self, page):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=int, location='args', required=True)
        parser.add_argument('status', type=int, location='args', default=0)
        args = parser.parse_args()
        bids = UserModel.query.get(args.userid).bidProjects

        if args.status:
            bids = bids.filter(BidModel.project.has(ProjectModel.status == args.status))
        
        bids = bids.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = bids.total,
            pages = bids.pages,
            page = bids.page,
            per_page = bids.per_page,
            has_next = bids.has_next,
            has_prev = bids.has_prev,
            next_num = bids.next_num,
            prev_num = bids.prev_num,
            data=[e.serialize() for e in bids.items])

from sqlalchemy import or_
class ProjectList(Resource):
    def get(self, page):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('cid', type=int, location='args', default=0)
        get_parser.add_argument('keyword', type=str, location='args')
        get_parser.add_argument('status', type=int, location='args', default=0)
        get_parser.add_argument('orderby', type=int, location='args', choices=range(3), default=0)
        get_parser.add_argument('desc', type=int, location='args', choices=range(3), default=0)
        args = get_parser.parse_args()
        
        projects = ProjectModel.query

        if args.cid:
            projects = projects.filter( \
                or_( \
                    ProjectModel.categorys.any(CategoryModel.id == args.cid), \
                    ProjectModel.categorys.any(CategoryModel.parent_id == args.cid), \
                    ProjectModel.categorys.any(CategoryModel.parent.has(CategoryModel.parent_id == args.cid))
                    ) \
                )

        if args.keyword:
            projects = projects.filter(ProjectModel.name.contains(args.keyword))

        if args.status:
            projects = projects.filter(ProjectModel.status == args.status)
            
        if args.orderby == 1:
            if args.desc == 1:
                projects = projects.order_by(ProjectModel.publishDate.desc())
            else:
                projects = projects.order_by(ProjectModel.publishDate.asc())
        if args.orderby == 2:
            if args.desc == 1:
                projects = projects.order_by(ProjectModel.bonus.desc())
            else:
                projects = projects.order_by(ProjectModel.bonus.asc())

        projects = projects.paginate(page, app.config['POSTS_PER_PAGE'], False)

        return jsonify(total = projects.total,
            pages = projects.pages,
            page = projects.page,
            per_page = projects.per_page,
            has_next = projects.has_next,
            has_prev = projects.has_prev,
            next_num = projects.next_num,
            prev_num = projects.prev_num,
            data=[e.serialize() for e in projects.items])

