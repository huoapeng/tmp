
from flask import url_for

class ProjectDetailView(object):

    def __init__(self, 
            project,
            userid,
            userName,
            userLocation,
            category_str_list,
        ):
        self.project = project
        self.userid = userid
        self.userName = userName
        self.userLocation = userLocation
        self.category_str_list = category_str_list

    def serialize(self):
        return {
            'project': self.project.serialize(),
            'userid': self.userid,
            'userName': self.userName,
            'userLocation': self.userLocation,
            'userURI': url_for('.user', userid=self.userid, _external=True),
            'categoryString': ','.join(self.category_str_list)
        }

