# -*- coding: utf-8 -*-
import json
import logging

import requests
from flask import request, render_template, make_response, jsonify
from flask.ext.login import login_required, current_user

from leancloud import user, Query, LeanCloudError

from .musics import download_music
from utils import redis_op, format
from . import music as music_blueprint
from ..models import MusicSearchHistory, MusicFavorite, Music


@music_blueprint.route('')
def index():
    return render_template('music/index.html')


@music_blueprint.route('/api/get_musics')
def api_get_musics():
    keyword = request.args.get('keyword', '')
    musics = []
    if keyword:
        url = u"http://so.ard.iyyin.com/s/song_with_out?q=%s&page=1&size=20" % keyword
        response = requests.get(url)
        musics = json.loads(response.text).get('data')
    valid_musics = []

    music_favorite_data_object = {}

    # 把有效的音乐获取出来
    for music in musics:
        if not music.get('out_list'):
            music_favorite_data_object[music.get('song_id')] = False
            valid_musics.append(music)

    download_music(valid_musics)

    # 获取用户喜欢的音乐
    musics_favorite = []
    if current_user.is_authenticated():
        musics_favorite = Query(MusicFavorite) \
            .equal_to('user', user.User.create_without_data(current_user.id)) \
            .contained_in('song_id', [music.get('song_id') for music in valid_musics]) \
            .find()

    for music_favorite in musics_favorite:
        music_favorite_data_object[music_favorite.song_id] = True

    for music in valid_musics:
        music['is_like'] = music_favorite_data_object[music.get('song_id')]

    # redis_op.notify('channel:music:download', event={
    #     'musics': valid_musics
    # })
    return make_response(json.dumps(valid_musics))


@music_blueprint.route('/api/music_search_history', methods=['GET', 'POST'])
def api_music_search_history():
    keyword = request.json.get('keyword')
    music_search = MusicSearchHistory()
    music_search.set('keyword', keyword)
    if current_user.is_authenticated():
        music_search.set('user', user.User.create_without_data(current_user.id))
    music_search.save()
    return jsonify(save=True)


@music_blueprint.route('/api/music_favorite', methods=['GET', 'POST', 'DELETE'])
def api_music_favorite():
    if current_user.is_authenticated():
        if request.method == 'POST':
            song_id = int(request.json.get('song_id'))
            if Query(MusicFavorite)\
                    .equal_to('user', user.User.create_without_data(current_user.id))\
                    .equal_to('song_id', song_id).find():
                return jsonify(success=True)
            music_favorite = MusicFavorite()
            music_favorite.set('user', user.User.create_without_data(current_user.id))
            music_favorite.set('song_id', song_id)
            music_favorite.save()
            return jsonify(success=True)
        elif request.method == 'DELETE':
            song_id = int(request.json.get('song_id'))
            try:
                music_favorite = Query(MusicFavorite)\
                        .equal_to('user', user.User.create_without_data(current_user.id))\
                        .equal_to('song_id', song_id).first()
            except LeanCloudError as e:
                logging.warn(e.message)
            else:
                music_favorite.destroy()
            return jsonify(success=True)
        elif request.method == 'GET':
            music_favorites = Query(MusicFavorite)\
                .equal_to('user', user.User.create_without_data(current_user.id)).limit(20).find()
            favorite_musics = Query(Music)\
                .contained_in('song_id', [music_favorite.song_id for music_favorite in music_favorites])\
                .include('file.url')\
                .include('picture.url')\
                .find()
            results = []
            for music in favorite_musics:
                _music = format.format_music(music)
                _music['is_like'] = True
                results.append(_music)
            return make_response(json.dumps(results))
    else:
        return jsonify(success=False), 401
