# coding=utf-8
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.order import OrderModel
from myapi.model.user import UserModel
from myapi.model.work import WorkModel
from myapi.model.enum import order_status


class Order(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(
            'name', type=str, location='json', required=True)
        post_parser.add_argument(
            'buyerid', type=int, location='json', required=True)
        post_parser.add_argument(
            'sellerid', type=int, location='json', required=True)
        post_parser.add_argument(
            'workid', type=int, location='json', required=True)
        args = post_parser.parse_args()

        work = WorkModel.query.get(args.workid)

        order = OrderModel(args.name, work.price)
        db.session.add(order)

        work.orders.append(order)

        buyer = UserModel.query.get(args.buyerid)
        buyer.boughtOrders.append(order)

        seller = UserModel.query.get(args.sellerid)
        seller.soldOrders.append(order)

        db.session.commit()

        return order.serialize()


class UserBoughtOrders(Resource):
    def get(self, page):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=int, location='args', required=True)
        args = parser.parse_args()
        orders = UserModel.query.get(args.userid).boughtOrders

        orders = orders.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total=orders.total,
                       pages=orders.pages,
                       page=orders.page,
                       per_page=orders.per_page,
                       has_next=orders.has_next,
                       has_prev=orders.has_prev,
                       next_num=orders.next_num,
                       prev_num=orders.prev_num,
                       data=[e.serialize() for e in orders.items])


class UserSoldOrders(Resource):
    def get(self, page):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=int, location='args', required=True)
        args = parser.parse_args()
        orders = UserModel.query.get(args.userid).soldOrders

        orders = orders.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total=orders.total,
                       pages=orders.pages,
                       page=orders.page,
                       per_page=orders.per_page,
                       has_next=orders.has_next,
                       has_prev=orders.has_prev,
                       next_num=orders.next_num,
                       prev_num=orders.prev_num,
                       data=[e.serialize() for e in orders.items])
