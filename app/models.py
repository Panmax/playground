# -*- coding: utf-8 -*-
# @Author: 'Panmax'
from flask.ext.login import UserMixin

from leancloud import Query
from leancloud import Object as LObject
from leancloud import user


class _User(UserMixin, LObject):
    @property
    def username(self):
        return self.get('username')

    @property
    def email(self):
        return self.get('email')

    @classmethod
    def login(cls, email, password):
        try:
            u = Query(cls).equal_to('email', email).first()
            user.User().login(u.username, password)
        except Exception, e:
            print e
            return None
        return u

    @classmethod
    def register(cls, email, username, password):
        u = user.User(username=username, password=password, email=email)
        u.sign_up()
        u = Query(cls).equal_to('username', username).first()
        return u

    @classmethod
    def check_email_exist(cls, email):
        if Query(cls).equal_to('email', email).find():
            return True
        return False

    @classmethod
    def check_username_exist(cls, username):
        if Query(cls).equal_to('username', username).find():
            return True
        return False


class Music(LObject):
    @property
    def song_name(self):
        return self.get('song_name')

    @song_name.setter
    def song_name(self, s):
        self.set('song_name', s)

    @property
    def singer_name(self):
        return self.get('singer_name')

    @singer_name.setter
    def singer_name(self, s):
        self.set('singer_name', s)

    @property
    def song_id(self):
        return self.get('song_id')

    @song_id.setter
    def song_id(self, s):
        self.set('song_id', s)

    @property
    def singer_id(self):
        return self.get('singer_id')

    @singer_id.setter
    def singer_id(self, s):
        self.set('singer_id', s)

    @property
    def album_id(self):
        return self.get('album_id')

    @album_id.setter
    def album_id(self, a):
        self.set('album_id', a)

    @property
    def album_name(self):
        return self.get('album_name')

    @album_name.setter
    def album_name(self, a):
        self.set('album_name', a)

    @property
    def bit_rate(self):
        return self.get('bitRate')

    @bit_rate.setter
    def bit_rate(self, b):
        self.set('bitRate', b)

    @property
    def duration(self):
        return self.get('duration')

    @duration.setter
    def duration(self, d):
        self.set('duration', d)

    @property
    def suffix(self):
        return self.get('suffix')

    @suffix.setter
    def suffix(self, s):
        self.set('suffix', s)

    @property
    def type_description(self):
        return self.get('typeDescription')

    @type_description.setter
    def type_description(self, t):
        self.set('typeDescription', t)

    @property
    def size(self):
        return self.get('size')

    @size.setter
    def size(self, s):
        self.set('size', s)

    @property
    def file(self):
        return self.get('file')

    @file.setter
    def file(self, f):
        self.set('file', f)


class MusicSearchHistory(LObject):
    @property
    def keyword(self):
        return self.get('keyword')

    @property
    def user(self):
        return self.get('user')


class MusicFavorite(LObject):
    @property
    def user(self):
        return self.get('user')

    @property
    def song_id(self):
        return self.get('song_id')
