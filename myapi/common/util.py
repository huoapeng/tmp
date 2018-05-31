
# @staticmethod
def valid_email(value):
    import re
    m = re.match(r'(\w+)@(\w+)[.](\w+)', value)
    if m is None:
        raise ValueError("pls check email")
    
    return value

def md5(str):
    import hashlib
    import types
    if type(str) is types.StringType:
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()
    else:
        return ''

from flask.ext.restful import fields
class itemStatus(fields.Raw):
    def format(self, value):
        return "Normal" if value == 1 else "Delete"

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

