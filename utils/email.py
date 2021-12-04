# -*- coding: utf-8 -*-
import datetime
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import hashlib
import random
from smtplib import SMTP_SSL
from typing import Any

from utils.db import Db


HOST_SEVER = 'smtp.163.com'
SENDER = 'Sakuyark@163.com'
PWD = 'JKXUTNJUDVRDGTTV'
'''
    <div>
        <div style="margin:0;">
            <span style="font-size: 18px;">您好：</span>
        </div>
        <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">
            <div style="margin:0;">
                <span style="font-size: 18px;">这里是Sakuyark，您的账户：{data['user']}。</span>
            </div>
            <div style="margin:0;">
                <span style="font-size: 18px;">请点击下方链接激活账号</span>
            </div>
            <div style="margin:0;">
                <br />
            </div>
            <div style="text-align: left; margin: 0px;"></div>
        </blockquote>
    </div>
    <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">
        <div>
            <a href="https://www.sakuyark.com/login/activate/{key}" 
                style="font-size: 18px; text-decoration: underline;">
                <span style="font-size: 18px;">https://www.sakuyark.com/login/activate/{key}</span>
            </a>
        </div>
    </blockquote>'''


def send_verify_mail(
    collection: 'tuple[Db, str]',
    receiver: str,
    user: str,
    title: str,
    action: str,
    payload: str,
    data: Any,
    survival_time: datetime.timedelta = datetime.timedelta(hours=24)
) -> str:
    """
    发送验证邮件, 返回key
    :param collection: 数据库和集合
    :param receiver: 收件人
    :param user: 用户账户名称
    :param title: 验证内容标题
    :param action: 行为，将会显示为 请点击下方链接 + action
    :param payload: 验证链接前缀 生成的链接： payload + / + key
    :param data: 键值对的数据
    :param survival_time: 存活时间
    """
    key = collection[0].create_kv_pairs(collection[1], data, survival_time)
    mail_content = f'''
    <div>
        <div style="margin:0;">
            <span style="font-size: 18px;">您好：</span>
        </div>
        <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">
            <div style="margin:0;">
                <span style="font-size: 18px;">这里是Sakuyark，您的账户：{user}。</span>
            </div>
            <div style="margin:0;">
                <span style="font-size: 18px;">请点击下方链接{action}</span>
            </div>
            <div style="margin:0;">
                <br />
            </div>
            <div style="text-align: left; margin: 0px;"></div>
        </blockquote>
    </div>
    <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">
        <div>
            <a href="{payload}/{key}" 
                style="font-size: 18px; text-decoration: underline;">
                <span style="font-size: 18px;">{payload}/{key}</span>
            </a>
        </div>
    </blockquote>'''
    if not send_mail(receiver, title, mail_content):
        raise RuntimeError('邮件发送失败')
    return key


def send_verify_code(
    receiver: str,
    user: 'str | None' = None,
    title: str = '验证码',
    survival_time: datetime.timedelta = datetime.timedelta(minutes=10)
) -> 'tuple[str, datetime.datetime]':
    """
    发送验证码，返回 code
    :param receiver: 收件人
    :param user: 用户账户名称
    :param title: 验证内容标题
    :param data: 键值对的数据
    :param survival_time: 存活时间
    """
    code = random.randint(100000, 999999)
    mail_content = f"""
<div>
    <base target="_blank" />
    <style type="text/css">::-webkit-scrollbar{{ display: none; }}</style>
    <style id="cloudAttachStyle" type="text/css">#divNeteaseBigAttach, #divNeteaseBigAttach_bak{{display:none;}}</style>
    <style id="blockquoteStyle" type="text/css">blockquote{{display:none;}}</style>
    <style type="text/css">
        body{{font-size:14px;font-family:arial,verdana,sans-serif;line-height:1.666;padding:0;margin:0;overflow:auto;white-space:normal;word-wrap:break-word;min-height:100px}}
        td, input, button, select, body{{font-family:Helvetica, 'Microsoft Yahei', verdana}}
        pre {{white-space:pre-wrap;white-space:-moz-pre-wrap;white-space:-pre-wrap;white-space:-o-pre-wrap;word-wrap:break-word;width:95%}}
        th,td{{font-family:arial,verdana,sans-serif;line-height:1.666}}
        img{{ border:0}}
        header,footer,section,aside,article,nav,hgroup,figure,figcaption{{display:block}}
        blockquote{{margin-right:0px}}
    </style>


<table width="700" border="0" align="center" cellspacing="0" style="width:700px;">
    <tbody>
    <tr>
        <td>
            <div style="width:700px;margin:0 auto;border-bottom:1px solid #ccc;margin-bottom:30px;">
                <table border="0" cellpadding="0" cellspacing="0" width="700" height="39" style="font:12px Tahoma, Arial, 宋体;">
                    <tbody><tr><td width="210"></td></tr></tbody>
                </table>
            </div>
            <div style="width:680px;padding:0 10px;margin:0 auto;">
                <div style="line-height:1.5;font-size:14px;margin-bottom:25px;color:#4d4d4d;">
                    <strong style="display:block;margin-bottom:15px;">尊敬的用户，<span style="color:#f60;font-size: 16px;">{user or ''}</span>您好！</strong>
                    <strong style="display:block;margin-bottom:15px;">
                        您正在进行<span style="color: red">注册账号</span>操作，请在验证码输入框中输入：<span style="color:#f60;font-size: 24px">{code}</span>，以完成操作。
                    </strong>
                </div>
                <div style="margin-bottom:30px;">
                    <small style="display:block;margin-bottom:20px;font-size:12px;">
                        <p style="color:#747474;">
                            注意：为保证您的账号安全，请在<span style="color:#f60;font-size: 16px;">{int(survival_time.total_seconds()/60)}</span>内完成验证
                            <br/>
                            （工作人员不会向你索取此验证码，请勿泄漏！）
                        </p>
                    </small>
                </div>
            </div>
            <div style="width:700px;margin:0 auto;">
                <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                    <p>此为系统邮件，请勿回复<br />
                        请保管好您的邮箱，避免账号被他人盗用
                    </p>
                    <p>Sakuyark</p>
                </div>
            </div>
        </td>
    </tr>
    </tbody>
</table>

<br /></div>
"""
    if not send_mail(receiver, title, mail_content):
        raise RuntimeError('邮件发送失败')
    return code, datetime.datetime.now() + survival_time


def send_mail(receiver: str, mail_title: str, mail_content: str) -> bool:
    """
    发送邮件
    :param receiver: 收件人
    :param mail_title: 邮件标题
    :param mail_content: 邮件内容
    """
    msg = MIMEText(mail_content, "html", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = SENDER
    msg["To"] = receiver
    try:
        smtp = SMTP_SSL(HOST_SEVER)
        smtp.ehlo(HOST_SEVER)
        smtp.login(SENDER, PWD)
        smtp.sendmail(SENDER, receiver, msg.as_string())
        smtp.quit()
        return True
    except smtplib.SMTPException as e:
        print(f'邮件发送 产生错误：{e}')
        return False
