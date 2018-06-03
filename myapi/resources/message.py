from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.note import NoteModel
from myapi.model.message import NoteMessageModel, WorkMessageModel
from myapi.model.user import UserModel
from myapi.model.work import WorkModel

noteparser = reqparse.RequestParser()
noteparser.add_argument('message', type=str, location='json', required=True)
noteparser.add_argument('noteid', type=int, location='json', required=True)
noteparser.add_argument('userid', type=int, location='json', required=True)

note_message_result_field = {
    'id': fields.Integer,
    'message': fields.String,
    'publishDate': fields.DateTime,
    'note_id': fields.Integer,
    'user_id': fields.Integer
}

class NoteMessage(Resource):
    def get(self):
        pass

    @marshal_with(note_message_result_field)
    def post(self):
        args = noteparser.parse_args()
        message = NoteMessageModel(args.message)
        db.session.add(message)

        note = NoteModel.query.get(args.noteid)
        note.messages.append(message)

        user = UserModel.query.get(args.userid)
        user.notemessages.append(message)
        db.session.commit()
        return message

    def put(self):
        pass

    def delete(self):
        pass

class NoteMessageList(Resource):
    def get(self, noteid):
        messages = NoteMessageModel.query.filter_by(note_id=noteid).all()
        return jsonify(data=[e.serialize() for e in messages])

workparser = reqparse.RequestParser()
workparser.add_argument('message', type=str, location='json')
workparser.add_argument('workid', type=int, location='json')
workparser.add_argument('buyerid', type=int, location='json')
workparser.add_argument('sellerid', type=int, location='json')

work_message_result_field = {
    'id': fields.Integer,
    'message': fields.String,
    'publishDate': fields.DateTime,
    'work_id': fields.Integer,
    'buyer_id': fields.Integer,
    'seller_id': fields.Integer
}

class WorkMessage(Resource):
    def get(self):
        pass

    @marshal_with(work_message_result_field)
    def post(self):
        args = workparser.parse_args()
        print args
        message = WorkMessageModel(args.message)
        db.session.add(message)

        work = WorkModel.query.get(args.workid)
        work.messages.append(message)

        buyer = UserModel.query.get(args.buyerid)
        buyer.buyerMessages.append(message)

        seller = UserModel.query.get(args.sellerid)
        seller.sellerMessages.append(message)

        db.session.commit()
        return message

class WorkMessageList(Resource):
    def get(self, workid, buyerid, sellerid):
        messages = WorkMessageModel.query.filter_by(work_id=workid).filter_by(buyer_id=buyerid).filter_by(seller_id=sellerid).all()
        return jsonify(data=[e.serialize() for e in messages])

# class VersionMessage(Resource):
#     def get(self):
#         pass

#     @marshal_with(result_field)
#     def post(self):
#         args = parser.parse_args()
#         message = VersionMessageModel(args.message)
#         db.session.add(message)

#         version = VersionModel.query.get(args.belong_id)
#         version.messages.append(message)

#         user = UserModel.query.get(args.user_id)
#         user.versionmessages.append(message)
#         db.session.commit()
#         return message

#     def put(self):
#         pass

#     def delete(self):
#         pass

# class VersionMessageList(Resource):
#     @marshal_with(result_field)
#     def get(self, versionid):
#         version = VersionModel.query.get(versionid)
#         return version.messages
