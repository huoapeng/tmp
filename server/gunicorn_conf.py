import multiprocessing

bind = '127.0.0.1:6000'
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 2048
worker_class = "gevent"
debug = True
proc_name = 'gunicorn.proc'
pidfile = '/tmp/gunicorn.pid'
logfile = '/tmp/gunicorn.log'
loglevel = 'debug'