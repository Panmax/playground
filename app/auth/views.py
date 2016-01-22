# -*- coding: utf-8 -*-
# @Author: 'Panmax'
from flask import request, render_template, redirect, url_for, flash
from flask.ext.login import login_user, login_required, logout_user

from leancloud import Query

from . import auth
from .forms import RegistrationForm, LoginForm

from ..models import _User as User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.register(form.email.data.lower(), form.username.data, form.password.data)
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login(form.email.data.lower(), form.password.data)
        if user is not None:
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash(u'用户名或密码错误!')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'已退出登录')
    return redirect(url_for('main.index'))


@auth.route('/password_reset_request')
def password_reset_request():
    pass
