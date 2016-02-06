# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class JoinForm(Form):
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder': u'이메일을 입력하세요.'}
    )
    password = PasswordField(
        u'패스워드',
        [validators.data_required(u'패스워드를 입력하시기 바랍니다.'),
        validators.EqualTo('confirm_password', message=u'패스워드가 일치하지 않습니다.')],
        description={'placeholder': u'패스워드를 입력하세요.'}
    )
    confirm_password = PasswordField(
        u'패스워드 확인',
        [validators.data_required(u'패스워드를 한번 더 입력하세요.')],
        description={'placeholder': u'패스워드를 한번 더 입력하세요.'}
    )
    name = StringField(
        u'이름',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'}
    )

class LoginForm(Form):
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder': u'이메일을 입력하세요.'}
    )
    password = PasswordField(
        u'패스워드',
        [validators.data_required(u'패스워드를 입력하시기 바랍니다.'),
        validators.EqualTo('confirm_password', message=u'패스워드가 일치하지 않습니다.')],
        description={'placeholder': u'패스워드를 입력하세요.'}
    )