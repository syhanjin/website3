# -*- coding: utf-8 -*-
from flask.json import jsonify
from flask.wrappers import Response
import json
import hashlib
import datetime
import random


def make_key():
    return hashlib.md5(
        str(
            datetime.datetime.now().timestamp()*100000 + random.randint(10, 99)
        ).encode('utf-8')
    ).hexdigest()


def make_result_json(resp: Response) -> Response:
    """
    将数据请求类外包装
    """
    data = json.loads(resp.data)
    if 'code' in data:
        return jsonify(data)
    return jsonify({
        'code': 0,
        'data': data
    })
