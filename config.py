# -*- coding: utf-8 -*-
import os
__author__ = 'pan'


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        app.jinja_env.variable_start_string = '{{ '
        app.jinja_env.variable_end_string = ' }}'


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
