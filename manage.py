# -*- coding: utf-8 -*-
import os

from app import create_app

__author__ = 'pan'

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
