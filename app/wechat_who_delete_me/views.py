# -*- coding: utf-8 -*-
from flask import request
from flask import render_template

from . import wechat_who_delete_me
__author__ = 'pan'


@wechat_who_delete_me.route('')
def index():
    return render_template('wechat_who_delete_me/index.html')
