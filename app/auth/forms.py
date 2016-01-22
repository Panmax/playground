# -*- coding: utf-8 -*-
# @Author: 'Panmax'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from ..models import _User as User


class RegistrationForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 254), Email()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(5, 64),
                                       Regexp('^[\u4e00-\u9fa5_a-zA-Z0-9]+$',
                                              message=u'用户名只能由中文,英文,数字组成')])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(6, 30), EqualTo('password2', message=u'两次密码必须相同')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.check_email_exist(field.data.lower()):
            raise ValidationError(u'该邮箱已被注册')

    def validate_username(self, field):
        if User.check_username_exist(field.data):
            raise ValidationError(u'用户名已被使用')


class LoginForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(6, 30)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField(u'登录')
