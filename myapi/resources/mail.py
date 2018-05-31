#coding=utf-8
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.mail import MailModel, MailTemplateModel, MailTriggerModel

class Mail(Resource):
    def get(self, id):
        return MailModel.query.get(id).serialize()

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('id', type=int, location='json', required=True)
        post_parser.add_argument('params', type=str, location='json', required=True)
        args = post_parser.parse_args()

        template = MailTemplateModel.query.get(args.id)
        title = template.title.replace(args.params)
        content = template.content.replace(args.params)

        mail = MailModel(title, content) 
        db.session.add(mail)
        db.session.commit()
        return mail.serialize()

class MailList(Resource):
    def get(self, page):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=int, location='args', required=True)
        args = parser.parse_args()

        mails = MailModel.query.filter_by(receiver_id = args.userid)
            .paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = mails.total,
            pages = mails.pages,
            page = mails.page,
            per_page = mails.per_page,
            has_next = mails.has_next,
            has_prev = mails.has_prev,
            next_num = mails.next_num,
            prev_num = mails.prev_num,
            data=[e.serialize() for e in mails.items])

class MailTemplate(Resource):
    def get(self, id):
        return MailTemplateModel.query.get(id).serialize()

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('title', type=str, location='json', required=True)
        post_parser.add_argument('content', type=str, location='json', required=True)
        post_parser.add_argument('description', type=str, location='json')
        args = post_parser.parse_args()

        template = MailTemplateModel(args.title, args.content, args.description) 
        db.session.add(template)
        db.session.commit()
        return template.serialize()

class MailTemplateList(Resource):
    def get(self, page):
        parser = reqparse.RequestParser()
        parser.add_argument('triggerid', type=int, location='args')
        args = parser.parse_args()

        templates = MailTemplateModel.query

        if args.triggerid:
            templates = templates.filter_by(trigger_id = args.triggerid)

        templates = templates.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = templates.total,
            pages = templates.pages,
            page = templates.page,
            per_page = templates.per_page,
            has_next = templates.has_next,
            has_prev = templates.has_prev,
            next_num = templates.next_num,
            prev_num = templates.prev_num,
            data=[e.serialize() for e in templates.items])

class MailTrigger(Resource):
    def get(self, id):
        trigger = MailTriggerModel.query.get(id)
        return trigger.serialize()

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', type=str, location='json', required=True)
        args = post_parser.parse_args()

        trigger = MailTriggerModel(args.name) 
        db.session.add(trigger)
        db.session.commit()
        return trigger.serialize()

    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('triggerid', type=int, location='json', required=True)
        post_parser.add_argument('templateid', type=int, location='json', required=True)
        args = post_parser.parse_args()

        trigger = MailTriggerModel.query.get(args.triggerid)
        tempmlate = MailTemplateModel.query.get(args.templateid)
        trigger.templates.append(template)
        db.session.commit()

class MailTriggerList(Resource):
    def get(self, page):

        triggers = MailTemplateModel.query.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = triggers.total,
            pages = triggers.pages,
            page = triggers.page,
            per_page = triggers.per_page,
            has_next = triggers.has_next,
            has_prev = triggers.has_prev,
            next_num = triggers.next_num,
            prev_num = triggers.prev_num,
            data=[e.serialize() for e in triggers.items])

