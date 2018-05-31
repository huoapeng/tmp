from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.note import NoteModel
from myapi.model.user import UserModel
from myapi.model.project import ProjectModel
# from myapi.model.enum import note_status
from myapi.common.util import itemStatus

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, location='json', required=True)
parser.add_argument('projectid', type=int, location='json', required=True)
parser.add_argument('userid', type=int, location='json', required=True)

note_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'publishDate': fields.DateTime,
    'status':  itemStatus(attribute='status'),
    'user_id': fields.Integer,
    'project_id': fields.Integer
}

class Note(Resource):
    @marshal_with(note_fields)
    def get(self, noteid):
        return NoteModel.query.get(noteid)

    @marshal_with(note_fields)
    def post(self):
        args = parser.parse_args()
        note = NoteModel(args.title)
        db.session.add(note)

        project = ProjectModel.query.get(args.projectid)
        project.notes.append(note)

        user = UserModel.query.get(args.userid)
        user.notes.append(note)
        db.session.commit()
        return note

    def put(self):
        pass

    @marshal_with(note_fields)
    def delete(self):
        args = parser.parse_args()
        note = NoteModel.query.get(args.id)
        note.status = version_status.delete
        db.session.commit()
        return note

class ProjectNotes(Resource):
    def get(self, projectid):
        notes = NoteModel.query.filter_by(project_id=projectid).order_by(NoteModel.publishDate.desc()).all()
        return jsonify(data=[e.serialize() for e in notes])

