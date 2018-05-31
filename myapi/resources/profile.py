#coding=utf-8
from flask import jsonify, url_for
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel
from myapi.common.util import itemStatus

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', required=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('owner_id', type=int, location='json', required=True)

resource_fields = {'project': itemStatus(attribute='status')}
resource_fields['list']={}
resource_fields['list']['sublist']={}

user_fields = {
    'projectName': fields.String,
    'projectKinds':fields.String
}

class ProjectView():
    def __init__(self, projectName, projectKinds=None):
        self.projectName = projectName
        self.projectKinds = projectKinds

data = {}

from myapi.resources.smtp import send

class Profile(Resource):
    # @marshal_with(user_fields)
    def get(self):
        return jsonify(result = send(["huoapeng@hippoanimation.com","huoapeng@animen.com.cn"], 'retrieve_password'))
        str_list = []

        project = ProjectModel.query.get(1)
        return jsonify({
            'projectName':project.name,
            'projectKinds':','.join(str_list),
            'url':url_for('.user', _external=True, userid=1),
            })

