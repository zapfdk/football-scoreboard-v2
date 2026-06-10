import multiprocessing
import os

_root = os.path.dirname(os.path.abspath(__file__))
_chdir = os.path.join(_root, 'football_scoreboard')

bind = os.environ.get('GUNICORN_BIND', '127.0.0.1:8000')
workers = int(os.environ.get('GUNICORN_WORKERS', max(2, multiprocessing.cpu_count() // 2)))
worker_class = 'uvicorn.workers.UvicornWorker'
chdir = _chdir
pythonpath = _chdir
wsgi_app = 'football_scoreboard.routing:application'
timeout = 120
keepalive = 5
accesslog = '-'
errorlog = '-'
raw_env = ['DJANGO_SETTINGS_MODULE=football_scoreboard.settings']
