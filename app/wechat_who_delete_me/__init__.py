# -*- coding: utf-8 -*-
from flask import Blueprint

__author__ = 'pan'

wechat_who_delete_me = Blueprint('wechat_who_delete_me', __name__)

from . import views
