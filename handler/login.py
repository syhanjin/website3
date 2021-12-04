# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, session, request
from werkzeug.utils import redirect

from utils.user import User
from utils import template, db, email

login = Blueprint('login', __name__, url_prefix='/login')


@login.route('/', methods=['GET'])
def login_main():
    if User.check_uid(request, session):
        return redirect('/', 301)
    return template.page(request, 'login', 'main')


@login.route('/retrieve', methods=['GET'])
def login_retrieve():

    return template.page(request, 'login', 'retrieve')


@login.route('/retrieve/reset/<string:key>', methods=['GET'])
def login_retrieve_reset(key):
    if key is None:
        return template.error(request, '请传入key值')
    if not db.user.has_kv_pairs('retrieve', key):
        return template.error(request, '该key不存在或已过期')
    return template.page(
        request, 'login', 'retrieve_reset', key=key
    )


# QQ 登录
@login.route('/qq')
def login_qq():
    if request.args.get('state') != 'login':
        return redirect('/', 301)
    code = request.args.get('code')
    if code is None:
        return redirect('/', 301)
    data = User.get_qq_data(code)
    user = User(qq_open_id=data['openid'])
    if user.error is not None:
        key = db.user.create_kv_pairs(
            'qq_login', data, datetime.timedelta(hours=24)
        )
        return redirect(f'/login/qq/new?key={key}')
    session['_uid'] = user.uid
    session['logintime'] = str(datetime.datetime.now())
    user.setutime()
    resp = redirect(session.get('last') or '/')
    resp.set_cookie('_uid', str(user.uid))
    return resp


@login.route('/qq/new', methods=['GET'])
def login_qq_new():
    key = request.args.get('key')
    if key is None:
        return template.error(request, '请传入key值')
    if not db.user.has_kv_pairs('qq_login', key):
        return template.error(request, '该key不存在或已过期')
    return template.page(
        request, 'login', 'qq/new', key=key
    )


# 表单
@login.route('/retrieve/reset/<string:key>', methods=['POST'])
def login_retrieve_reset_(key):
    if key is None:
        return template.error(request, '请传入key值')
    if not db.user.has_kv_pairs('retrieve', key):
        return template.error(request, '该key不存在或已过期')
    pwd1 = request.form.get('pwd1')
    pwd2 = request.form.get('pwd2')
    if pwd1 == None or pwd2 == None:
        return template.error(request, '数据有误')
    if not pwd2 == pwd1:
        return template.error(request, '两次密码不一样')
    _uid = db.user.get_kv_pairs('retrieve', key)['_uid']
    user = User(_uid)
    user.setpwd(pwd1, check_old=False)
    user.save()
    return template.page(request, 'login', 'retrieve_success')


@login.route('/qq/new', methods=['POST'])
def login_qq_new_post():
    key = request.form.get('key')
    if key is None:
        return {'code': 1, 'error': 'key'}
    qq_data = db.user.get_kv_pairs('qq_login', key)
    if qq_data is None:
        return {'code': 1, 'error': 'key'}
    user = request.form.get('user')
    if user is None:
        return {'code': 1, 'error': 'user'}
    if User.has_user(user):
        return {'code': 1, 'error': 'user is exist'}
    data = {
        'qq_data': qq_data,
        'user': user
    }
    User.register_user(data)
    user = User(qq_open_id=qq_data['openid'])
    session['_uid'] = user.uid
    session['logintime'] = str(datetime.datetime.now())
    user.setutime()
    user.save()
    resp = redirect(session.get('last') or '/')
    resp.set_cookie('_uid', str(user.uid))
    return resp


@login.route('/', methods=['POST'])
def login_post():
    un = request.form.get('user')
    pwd = request.form.get('pwd')
    if un is None or pwd is None:
        return template.page(request, 'login', 'main', warn=u'数据结构有误')
    if un == '':
        return template.page(request, 'login', 'main', warn=u'用户名不可为空')
    if pwd == '':
        return template.page(request, 'login', 'main',  warn=u'密码不可为空', user=un)
    if not User.has_user(un):
        return template.page(request, 'login', 'main',  warn=u'用户名或密码错误', user=un)
    user = User(user=un)
    if user.check_pwd(pwd):
        session['_uid'] = user.uid
        session['logintime'] = str(datetime.datetime.now())
        resp = redirect(session.get('last') or '/')
        resp.set_cookie('_uid', str(user.uid))
        return resp
    else:
        return template.page(request, 'login', 'main', warn=u'用户名或密码错误', user=un)


# 发送邮件
@login.route('/retrieve', methods=['POST'])
def login_retrieve_post():
    receiver = request.form.get('mail')
    if receiver is None:
        return template.error(request, '邮件错误')
    data = db.user.find('data', {'mail': receiver})
    if data is None:
        return '数据错误'
    _uid = data['_uid']
    key = email.send_verify_mail(
        (db.user, 'retrieve'),
        receiver, data['user'], '密码重置', '重置密码',
        'https://www.sakuyark.com/login/retrieve/reset',
        {'mail': receiver, '_uid': _uid}
    )
    return redirect('/login', 301)
