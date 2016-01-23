# -*- coding: utf-8 -*-
import json

import requests
from flask import render_template
from flask import request

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

    # download
    for music in valid_musics:
        song_name = music.get('song_name')
        song_id = music.get('song_id')
        singer_name = music.get('singer_name')
        singer_id = music.get('singer_id')
        audition_list = music.get('audition_list')
        #
        for audition in audition_list:
            url = audition.get('url')
            redis_op.notify('channel:music:download', event={
                'song_name': song_name,
                'song_id': song_id,
                'singer_name': singer_name,
                'singer_id': singer_id,
                'url': url
            })

    return render_template('music/index.html', musics=valid_musics, name=name)
