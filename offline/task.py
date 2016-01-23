#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'Panmax'
import logging
import redis
import gevent

from utils import redis_op


class OfflineTask(object):
    def __init__(self, redis_instance, channel=None):
        self._redis = None
        self._subscriber = None
        self._channel = channel or getattr(self, 'channel')
        self.connect(redis_instance)
        logging.info('Subscribed: %s', self._channel)

    def connect(self, redis_instance=None):
        try:
            self._redis = redis_instance or redis_op.init_redis()
            self._subscriber = self._redis.pubsub(ignore_subscribe_messages=True)
            self._subscriber.subscribe(self._channel)
        except redis.connection.ConnectionError as e:
            logging.error('Redis connect failed')
            gevent.sleep(0.2)
            self.connect()

    def reconnect(self):
        logging.info('Reconnect redis')
        gevent.sleep(0.2)
        self.reset()
        self.connect()

    def reset(self):
        logging.info('Reset redis')
        self._redis = None
        self._subscriber = None

    def loop(self):
        while True:
            try:
                self._loop()
            except redis.connection.ConnectionError as e:
                self.reconnect()

    def _loop(self):
        logging.info('loop: %s', self.__class__)
        try:
            for message in self._subscriber.listen():
                self.on_message(message)
        except redis.connection.ConnectionError as e:
            logging.error('on_message connection error: %s', e.message)
            raise e
        except Exception as e:
            logging.error('on_message error: %s', e.message)

    def on_message(self, message):
        raise Exception('Not implemented')
