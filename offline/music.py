#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'Panmax'

import json
import logging
import StringIO
import urllib2

from leancloud import File

from . import task


class Config(object):
    music_download_queue = 'channel:music:download'


class MusicDownload(task.OfflineTask):
    channel = Config.music_download_queue

    def on_message(self, message):
        logging.info(message)
        msg = json.loads(message['data'])
        url = msg.get('url')
        song_name = msg.get('song_name')
        filename = u'{}.mp3'.format(song_name)
        f = File(filename, StringIO.StringIO(urllib2.urlopen(url).read()))
        f.save()
