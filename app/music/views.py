# -*- coding: utf-8 -*-
import json

import requests
from flask import request, render_template, jsonify, make_response

from utils import redis_op
from . import music


@music.route('')
def index():
    name = request.args.get('name', '')
    musics = []
    if name:
        url = u"http://so.ard.iyyin.com/s/song_with_out?q=%s&page=1&size=10" % name
        response = requests.get(url)
        musics = json.loads(response.text).get('data')
    valid_musics = [music for music in musics if not music.get('out_list')]
    redis_op.notify('channel:music:download', event={
        'musics': valid_musics
    })

    return render_template('music/index.html', musics=valid_musics, name=name)


@music.route('/api/get_musics')
def api_get_musics():
    keyword = request.args.get('keyword', '')
    musics = []
    if keyword:
        url = u"http://so.ard.iyyin.com/s/song_with_out?q=%s&page=1&size=10" % keyword
        response = requests.get(url)
        musics = json.loads(response.text).get('data')
    valid_musics = [music for music in musics if not music.get('out_list')]
    return make_response(json.dumps(valid_musics))
