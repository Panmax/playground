# -*- coding: utf-8 -*-
import json

import requests
from flask import request, render_template, make_response, jsonify
from flask.ext.login import login_required, current_user

from leancloud import user

from utils import redis_op
from . import music
from ..models import MusicSearchHistory


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


@music.route('/api/music_search_history', methods=['GET', 'POST'])
def api_user_search():
    keyword = request.json.get('keyword')
    music_search = MusicSearchHistory()
    music_search.set('keyword', keyword)
    if current_user.is_authenticated():
        music_search.set('user', user.User.create_without_data(current_user.id))
    music_search.save()
    return jsonify(save=True)


@music.route('/api/user_info')
def api_user_info():
    is_login = False
    if current_user.is_authenticated():
        is_login = True
    return jsonify(is_login=is_login)
