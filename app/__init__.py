# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager

import gevent

from leancloud import Query

import offline

from config import config
from models import _User
from utils.redis_op import init_redis

__author__ = 'pan'
logging.basicConfig(level=logging.INFO)

bootstrap = Bootstrap()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    try:
        user = Query(_User).get(user_id)
    except Exception, e:
        print e
    else:
        return user


# def schedule():
#     for cls in offline.__all__:
#         instance = cls(init_redis())
#         gevent.spawn(instance.loop)
# schedule()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.register'
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .music import music as music_blueprint
    app.register_blueprint(music_blueprint, url_prefix='/music')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
