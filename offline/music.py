#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'Panmax'

import json
import logging
import StringIO
import urllib2

from leancloud import Query, File

from . import task
from app.models import Music


class Config(object):
    music_download_queue = 'channel:music:download'


class MusicDownload(task.OfflineTask):
    channel = Config.music_download_queue

    def on_message(self, message):
        logging.info(message)
        msg = json.loads(message['data'])
        musics = msg.get('musics')

        # download
        for music in musics:
            song_name = music.get('song_name')
            song_id = music.get('song_id')
            singer_name = music.get('singer_name')
            singer_id = music.get('singer_id')
            audition_list = music.get('audition_list')
            album_id = music.get('album_id')
            album_name = music.get('album_name')

            audition = audition_list[-1]
            url = audition.get('url')
            duration = audition.get('duration')
            suffix = audition.get('suffix')
            bit_rate = audition.get('bitRate')
            type_description = audition.get('typeDescription')
            size = audition.get('size')
            pic_url = music.get('mv_list')[0].get('pic_url') if music.get('mv_list') else ''

            if not Query(Music).equal_to('song_id', song_id).find():
                filename = u'{}-{}.mp3'.format(song_name, singer_name)
                f = File(filename, StringIO.StringIO(urllib2.urlopen(url).read()))
                f.save()

                picture = None
                if pic_url:
                    picture_name = u'{}-{}.jpg'.format(song_name, singer_name)
                    picture = File(picture_name, StringIO.StringIO(urllib2.urlopen(pic_url).read()))
                    picture.save()

                m = Music()
                m.file = f
                m.duration = duration
                m.suffix = suffix
                m.bit_rate = bit_rate
                m.type_description = type_description
                m.size = size
                m.song_name = song_name
                m.song_id = song_id
                m.singer_name = singer_name
                m.singer_id = singer_id
                m.album_id = album_id
                m.album_name = album_name
                if picture:
                    m.picture = picture
                m.save()
