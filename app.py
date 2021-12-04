# -*- coding: utf-8 -*-
"""
app.py
"""
from flask import Flask, session, redirect, request
from handler import login, register, api
import datetime
import utils
from utils import template, datas, text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sakuyark_secret_key_2021'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
# app.config['SERVER_NAME'] = 'sakuyark.com'
app.debug = True

# --


@app.route('/')
def home():
    session.permanent = True
    return template.page(request)


@app.errorhandler(404)
def handle_404_error(err_msg):

    return template._404_not_found(request)


@app.after_request
def handle_after_request(resp):
    try:
        if request.url.rsplit('.', 1)[1] == 'js':
            resp.mimetype = 'text/javascript'
    except:
        pass
    if resp.mimetype == 'application/json':
        return datas.make_result_json(resp)
    if resp.mimetype == 'text/html':
        # Updates Needed
        if not text.has(request.url, ['/static', '/login']):
            session['last'] = request.url
    return resp


# 注册
app.register_blueprint(login.login)
app.register_blueprint(register.rg)
app.register_blueprint(api.api)


# --

LocalIP = utils.get_host_ip()  # 获取ip
app.run(
    # host=LocalIP, port=443, ssl_context=('sakuyark.com.pem', 'sakuyark.com.key')
    host=LocalIP, port=80
)  # 启动服务器
