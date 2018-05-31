import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.sqlalchemy import SQLAlchemy
from json_app import make_json_app

db = SQLAlchemy()
app = make_json_app(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def create_app(config_name):
    app.config.from_object(config_name)
    #app.config.from_envvar('APP_CONFIG_FILE')

    db.init_app(app)

    from router import api_bp
    # api.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api/v1.0')
    return app
    
# @app.errorhandler(InvalidAPIUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
# @app.route('/foo')
# def get_foo():
#     raise InvalidUsage('This view is gone', status_code=410)