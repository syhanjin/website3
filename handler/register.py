# -*- coding: utf-8 -*-
from flask import Blueprint, request, session

import datetime
from utils import INITIAL_TIME, OK, TIME_FORMAT, template, email
from utils.user import User

rg = Blueprint('register', __name__, url_prefix='/register')


@rg.route('/', methods=['GET'])
def rg_main():

    return template.page(request, 'register', 'main')


@rg.route('/code', methods=['POST'])
def rg_code():
    receiver = str(request.form.get('mail'))
    if receiver is None:
        return {'code': 1, 'error': '邮箱错误'}
    code, deadline = email.send_verify_code(receiver, None, '注册验证')
    session['rg_mail'] = receiver
    session['rg_code'] = str(code)
    session['rg_deadline'] = str(deadline)
    return OK


@rg.route('/code/check', methods=['POST'])
def rg_code_check():
    mail = str(request.form.get('mail'))
    code = request.form.get('code')
    if (
        mail is None or code is None
        or datetime.datetime.now() > datetime.datetime.strptime(
            session.get('rg_deadline'),
            TIME_FORMAT
        ) if session.get('rg_deadline') else INITIAL_TIME
        or session.get('rg_mail') != mail
        or session.get('rg_code') != code
    ):
        return 'False'
    return 'True'


@rg.route('/', methods=['POST'])
def rg_post():
    deadline = datetime.datetime.strptime(
        session.get('rg_deadline'),
        TIME_FORMAT
    ) if session.get('rg_deadline') else INITIAL_TIME
    user = request.form.get('user')
    pwd1 = request.form.get('pwd1')
    pwd2 = request.form.get('pwd2')
    mail = request.form.get('mail')
    code = request.form.get('code')
    if user is None or User.has_user(user):
        return template.page(request, 'register', 'main', warn='用户名不可用')
    if (pwd1 or pwd2) is None or len(pwd1) < 8:
        return template.page(request, 'register', 'main', warn='密码太短')
    if pwd1 != pwd2:
        return template.page(request, 'register', 'main', warn='两次密码不匹配')
    if mail is None or mail != session.get('rg_mail'):
        return template.page(request, 'register', 'main', warn='邮箱不匹配')
    if code is None or datetime.datetime.now() > deadline or code != session.get('rg_code'):
        return template.page(request, 'register', 'main', warn='验证码错误')

    User.register_user({'user': user, 'pwd': pwd1, 'mail': mail})
    return template.page(request, 'register', 'success', url='/login')
