# -*- coding: utf-8 -*-
from flask import Blueprint

__author__ = 'pan'

music = Blueprint('music', __name__)

from . import views
