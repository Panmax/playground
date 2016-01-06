# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.bootstrap import Bootstrap

from config import config

__author__ = 'pan'

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .music import music as music_blueprint
    app.register_blueprint(music_blueprint, url_prefix='/music')

    from .wechat_who_delete_me import wechat_who_delete_me as wechat_who_delete_me_blueprint
    app.register_blueprint(wechat_who_delete_me_blueprint, url_prefix='/who-delete-me')

    return app
