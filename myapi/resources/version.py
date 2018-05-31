from flask import jsonify
from flask.ext.restful import Resource, fields, reqparse
from myapi import db
from myapi.model.version import VersionModel
from myapi.model.user import UserModel
from myapi.model.project import ProjectModel
from myapi.model.enum import version_status

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, location='json', required=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('image', type=str, location='json')
parser.add_argument('projectid', type=int, location='json', required=True)
parser.add_argument('userid', type=int, location='json', required=True)

class Version(Resource):
    def get(self, versionid):
        version = VersionModel.query.get(versionid)
        return jsonify(version.serialize())

    def post(self):
        args = parser.parse_args()
        version = VersionModel(args.title, args.description, args.image)
        db.session.add(version)

        project = ProjectModel.query.get(args.projectid)
        project.versions.append(version)

        user = UserModel.query.get(args.userid)
        user.versions.append(version)
        db.session.commit()
        return jsonify(version.serialize())

    def put(self):      
        pass

    def delete(self):
        args = parser.parse_args()
        version = VersionModel.query.get(args.id)
        version.status = version_status.delete
        db.session.commit()
        return jsonify(version.serialize())

class ProjectVersions(Resource):
    def get(self, projectid):
        versions = VersionModel.query\
            .filter_by(status = version_status.normal)\
            .filter_by(project_id = projectid)\
            .order_by(VersionModel.publishDate.desc()).all()
        return jsonify(data=[e.serialize() for e in versions])

