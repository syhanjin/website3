# -*- coding: utf-8 -*-
from flask import Blueprint, request, session

from utils.user import User
from utils import TIME_FORMAT, db

import datetime


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/has/user', methods=['POST'])
def api_has_user():
    un = str(request.form.get('user'))
    if User.has_user(un):
        return 'True'
    return 'False'


@api.route('/user/data', methods=['GET'])
def api_user_data():
    _uid = User.check_uid(request, session)
    user = User(_uid)
    if user.error is not None:
        session['_uid'] = 0
        return {'code': 3, 'error': f'{user.error} _uid={_uid}'}
    logintime = datetime.datetime.strptime(session.get('logintime'), TIME_FORMAT)
    pmodify = user.pmodify
    if logintime < pmodify:
        return {'code': 3, 'error': f'password has changed. logintime={logintime}, pmodify={pmodify}'}
    user.setutime()
    data = user.to_dict()
    # data['chat-count'] = chatdb.messages.find(
    #     {'read': False, 'r_uid': _uid}).count()
    return data