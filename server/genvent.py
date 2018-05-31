from gevent.wsgi import WSGIServer
from myapi import create_app

app = create_app('config.webapiconfig')
http_server = WSGIServer(('', 6000), app)
http_server.serve_forever()
