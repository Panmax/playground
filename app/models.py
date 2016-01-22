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
