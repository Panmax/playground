# -*- coding: utf-8 -*-
from flask import request
from flask import render_template

from . import music
__author__ = 'pan'


@music.route('/')
def index():
    return render_template('music/index.html')