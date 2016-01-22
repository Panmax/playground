# -*- coding: utf-8 -*-

from flask import render_template
from flask.ext.login import current_user

from . import main
__author__ = 'pan'


@main.route('/')
def index():
    return render_template('index.html')
