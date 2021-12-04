# -*- coding: utf-8 -*-
from flask.wrappers import Request
import socket
import datetime


INITIAL_TIME = datetime.datetime(2021, 6, 20)
LOGIN_EXP = 1
TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

"""
{'code': 0}
"""
OK = {'code': 0}


QQ_CLIENT_ID = 101978697
QQ_CLIENT_SECRET = '2247193aa54fa286182734a1863bdc63'  # key
QQ_REDIRECT_URI = 'https://sakuyark.com/login/qq'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.0.0.1', 8080))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def is_mobile(request: Request) -> bool:
    """
    判断用户是否为手机端
    """
    UserAgent = request.headers.get("User-Agent")
    for i in ['iPhone', 'iPod', 'Android', 'ios', 'iPad']:
        if i in UserAgent:
            return True
    return False
