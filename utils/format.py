#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'Panmax'


def format_music(music):
    _music = {
        'song_id': music.song_id,
        'song_name': music.song_name,
        'singer_name': music.singer_name,
        'album_name': music.album_name,
        'url': music.file.url,
        'pic_url': music.picture.url if music.picture else ''
    }
    return _music
