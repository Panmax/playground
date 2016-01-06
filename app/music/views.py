# -*- coding: utf-8 -*-
import requests
import json

from flask import request
from flask import render_template

from . import music
__author__ = 'pan'


@music.route('')
def index():
    name = request.args.get('name', '')
    musics = []
    if name:
        url = u"http://so.ard.iyyin.com/s/song_with_out?q=%s&page=1&size=10" % name
        response = requests.get(url)
        musics = json.loads(response.text).get('data')
    valid_musics = [music for music in musics if not music.get('out_list')]
    return render_template('music/index.html', musics=valid_musics, name=name)
