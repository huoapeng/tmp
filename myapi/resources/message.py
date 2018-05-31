from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.note import NoteModel
from myapi.model.message import NoteMessageModel
from myapi.model.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('message', type=str, location='json', required=True)
parser.add_argument('noteid', type=int, location='json', required=True)
parser.add_argument('userid', type=int, location='json', required=True)

result_field = {
    'id': fields.Integer,
    'message': fields.String,
    'publishDate': fields.DateTime,
    'note_id': fields.Integer,
    'user_id': fields.Integer
}

class NoteMessage(Resource):
    def get(self):
        pass

    @marshal_with(result_field)
    def post(self):
        args = parser.parse_args()
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
