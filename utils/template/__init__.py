# -*- coding: utf-8 -*-
from flask import render_template
from flask.wrappers import Request
import utils
from utils import db


def _404_not_found(request: Request, text: str = "404 Not Found!"):
    """
    404 页面
    """
    return error(request, text, 404)


def error(request: Request, error: str, code: int = 200):
    """
    错误页面
    """
    data = create_datas({})
    if utils.is_mobile(request):
        return render_template('error/m.html', error=error, data=data), code
    return render_template('error/pc.html', error=error, data=data), code


def page(request: Request, pre: str = '', sub: str = 'layout', data={}, **args) -> str:
    """
    返回页面
    :param request: Request
    :param pre: 包路径 主站为 ""
    :param sub: 页面路径，包+类型+页面路径.html 构成完整模板
    :param data: 传入的数据
    """
    type = 'm' if utils.is_mobile(request) else 'pc'
    data = create_datas(data)
    if pre == '':
        return render_template(f"{sub}/{type}.html", data=data, **args)
    return render_template(f"{pre}/{type}/{sub}.html", data=data, **args)


def create_datas(data) -> dict:
    
    tail_links = db.main.find('links', type=1, sort=('loca', 1))
    data['tail_links'] = tail_links
    return data