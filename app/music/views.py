# -*- coding: utf-8 -*-
import json

import requests
from flask import request, render_template, make_response

from utils import redis_op
from . import music


@music.route('')
def index():
    return render_template('music/index.html')


@music.route('/api/get_musics')
def api_get_musics():
    keyword = request.args.get('keyword', '')
    musics = []
    if keyword:
        url = u"http://so.ard.iyyin.com/s/song_with_out?q=%s&page=1&size=10" % keyword
        response = requests.get(url)
        musics = json.loads(response.text).get('data')
    valid_musics = []
    for music in musics:
        if not music.get('out_list'):
            music['is_like'] = False
            valid_musics.append(music)
    redis_op.notify('channel:music:download', event={
        'musics': valid_musics
    })
    return make_response(json.dumps(valid_musics))
