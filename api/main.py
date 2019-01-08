import configparser

from aiohttp import web

from routes import setup_routes
from db import db_middleware


def read_conf():
    config = configparser.ConfigParser()
    config.read('.env')
    return config


app = web.Application(middlewares=[db_middleware])
cnf = dict(read_conf().items('db'))

app['dsn'] = 'postgres://{user}:{password}@{host}:{port}/{database}'.format(
    user=cnf['postgres_user'],
    password=cnf['postgres_password'],
    host=cnf['host'],
    port=cnf['port'],
    database=cnf['postgres_db']
)
setup_routes(app)
web.run_app(app)
