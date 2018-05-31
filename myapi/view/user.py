from flask import url_for

class UserMarketView(object):

    def __init__(self, 
            user,
            tag_str_list
        ):
        self.user = user
        self.tag_str_list = tag_str_list

    def serialize(self):
        return {
            'user': self.user.serialize(),
            'tags': ','.join(self.tag_str_list)
        }

