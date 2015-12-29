# -*- coding: utf-8 -*-

from flask import render_template

from . import main
__author__ = 'pan'


@main.route('/')
def index():
    return render_template('index.html')
