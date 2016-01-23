#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'Panmax'
import os

import logging
import json
import redis
import gevent


def init_redis():
    if os.environ['LC_APP_ENV'] in ['stage', 'production']:
        uri = os.environ['REDIS_URL_cache']
    else:
        uri = 'redis://localhost:6379'
    _redis_client = redis.StrictRedis.from_url(uri, db=0)
    return _redis_client


def with_redis_connection(f, *args, **kwargs):
    _redis_client = init_redis()
    try:
        print 'Called', _redis_client
        logging.info('redis op: %s %s %s', _redis_client, args, kwargs)
        return f(_redis_client, *args, **kwargs)
    except redis.connection.ConnectionError as e:
        # reconnect on error
        gevent.sleep(0.01)
        raise e


def notify(channel, event):
    def f(r):
        logging.info('notify: %s %s', channel, event)
        return r.publish(channel, json.dumps(event))
    return with_redis_connection(f)
