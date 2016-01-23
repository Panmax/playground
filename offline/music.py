#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'Panmax'

import json
import logging

from leancloud import File

from . import task


class Config(object):
    music_download_queue = 'channel:music:download'


class MusicDownload(task.OfflineTask):
    channel = Config.music_download_queue

    def on_message(self, message):
        logging.info(message)
        logging.info('aaaaaa')
        msg = json.loads(message)
        url = msg.get('url')
        f = File.create_with_url('a.mp3', url)
        f.save()
