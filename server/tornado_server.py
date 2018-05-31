from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from myapi import create_app

app = create_app('config.webapiconfig')
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(6000)
IOLoop.instance().start()
