# -*- coding: utf-8 -*-
import datetime
import hashlib
import random
import requests

from utils import HEADERS, INITIAL_TIME, LOGIN_EXP, QQ_CLIENT_ID, QQ_CLIENT_SECRET, QQ_REDIRECT_URI


from utils import db


class User:
    """
    网站用户类
    :attr uid: int 用户id
    :attr user: str 用户名
    :attr pwd: str 密码MD5
    :attr photo: str 用户头像 bs4 or path
    :attr lvl: int 用户等级
    :attr exp: int 用户经验值
    :attr max_exp: int 该等级的最大经验值
    :attr admin: int 管理员级别 0~4
    :attr titles: list[dirc{class, text}] 用户头衔
    :attr pmodify: datetime 上次密码修改时间
    :attr umodify: datetime 上次用户名修改时间
    :attr last: datetime 上次登录时间
    :attr continuity: int 连续登录次数
    """
    attrs = [
        'user', 'pwd', 'photo', 'lvl', 'exp',
        'admin', 'titles', 'pmodify', 'umodify',
        'last', 'continuity', 'qq', 'qq_data',
    ]
    public = [
        'user', 'photo', 'lvl', 'exp', 'admin',
        'titles', 'pmodify', 'umodify', 'last',
        'continuity', 'qq'
    ]
    # region 初始值
    user = ''
    pwd = ''
    photo = ''
    lvl = 0
    exp = 0
    max_exp = 0
    admin = 0
    titles = []
    pmodify = INITIAL_TIME
    umodify = INITIAL_TIME
    last = INITIAL_TIME
    continuity = 0
    qq = 0
    qq_data = {}
    # endregion

    def __init__(
        self,
        _uid: 'int | None' = None,
        user: 'str | None' = None,
        qq_open_id: 'str | None' = None,
    ) -> None:
        self.error = None
        if _uid is not None:
            data = db.user.find('data', {'_uid': _uid})
            if data is None:
                self.error = f'无此用户 _uid={_uid}'
                return
        elif user is not None:
            data = db.user.find('data', {'user': user})
            if data is None:
                self.error = f'无此用户 user={user}'
                return
        elif qq_open_id is not None:
            data = db.user.find('data', {'qq_data.openid': qq_open_id})
            if data is None:
                self.error = f'qq 未注册'
                return
        else:
            self.error = f'缺少识别信息'
            return
        self.uid = data['_uid']
        for i in self.attrs:
            setattr(self, i, data.get(i) or getattr(self, i))
        lvldata = db.user.find('lvl', {'lvl': self.lvl})
        if lvldata is None:
            self.error = f'等级数据缺失 lvl={self.lvl}'
            return
        self.max_exp = lvldata['exp']

    def setuser(self, newuser: str) -> bool:
        """
        说明：
            设置用户名，成功返回True，失败返回False
        参数：
            :param newuser: 新用户名
        """
        data = db.user.find('data', {'user': newuser})
        if data is not None:
            return False
        self.user = newuser
        self.umodify = datetime.datetime.now()
        return True

    def add_exp(self, exp: int):
        """
        说明：
            增加经验值
        参数：
            :param exp: 添加的经验值
        """
        self.exp += exp
        if self.exp > self.max_exp:
            self.lvl += 1
            lvldata = db.user.find('lvl', {'lvl': self.lvl})
            if lvldata is None:
                self.error = f'等级数据缺失 lvl={self.lvl}'
                return False
            self.max_exp = lvldata['exp']
        return True

    def check_pwd(self, pwd: str) -> bool:
        """
        说明：
            检验密码
        参数：
            :param pwd: 密码
        """
        pwdmd5 = hashlib.md5(pwd.encode(encoding='UTF-8')).hexdigest()
        if pwdmd5 == self.pwd:
            # 在密码检验完成后自动处理登录时间
            self.setutime()
            return True
        return False

    def setutime(self):
        now = datetime.datetime.now()
        if (
                self.last is not None and
                now.year == self.last.year and
                now.month == self.last.month and
                now.day == self.last.day + 1
        ):
            self.continuity += 1
            self.add_exp(LOGIN_EXP)
        self.last = now
        self.save()

    def setpwd(self, new: str, old: str=None, check_old=True) -> bool:
        """
        说明：
            修改密码
        参数：
            :param new: 新密码
            :param old: 旧密码
            :param check_old: 是否检查原密码
        """
        if check_old and not self.check_pwd(old):
            return False
        self.pwd = hashlib.md5(new.encode(encoding='UTF-8')).hexdigest()
        return True

    def to_dict(self):
        data = {}
        for i in self.public:
            if i == 'umodify':
                if self.umodify is None:
                    data['umodify'] = 0
                else:
                    day = (datetime.datetime.now() - self.umodify).days
                    if day > 365:
                        data['umodify'] = 0
                    else:
                        data['umodify'] = 365-day
            else:
                data[i] = getattr(self, i, None)
        data['_uid'] = self.uid
        return data

    def save(self) -> None:
        """
        说明：
            保存修改，在处理最后必须调用！
        """
        data = {}
        for i in self.attrs:
            data[i] = getattr(self, i, None)
        db.user.update(
            'data',
            {'_uid': self.uid},
            {'$set': data}
        )

    @staticmethod
    def check_uid(request, session):
        _uid = request.cookies.get('_uid')
        if (
            (session.get('logintime') is None) or
            (_uid is None or _uid == '') or
            (int(_uid) != int(session.get('_uid')))
        ):
            print(session['_uid'], _uid)
            session['_uid'] = 0
            return None
        return int(_uid)

    @staticmethod
    def get_qq_data(code) -> dict:
        s = requests.Session()
        s.headers = HEADERS
        r = s.get(
            'https://graph.qq.com/oauth2.0/token',
            params={
                'grant_type': 'authorization_code',
                'client_id': QQ_CLIENT_ID,
                'client_secret': QQ_CLIENT_SECRET,
                'code': code,
                'redirect_uri': QQ_REDIRECT_URI,
                'fmt': 'json'
            }
        )
        result = {}
        data = r.json()
        result['access_token'] = data['access_token']
        result['expires_in'] = data['expires_in']
        result['refresh_token'] = data['refresh_token']
        r = s.get('https://graph.qq.com/oauth2.0/me',
                  params={'access_token': result['access_token'], 'fmt': 'json'})
        result['openid'] = r.json()['openid']
        return dict(result)

    @staticmethod
    def has_user(user: str) -> bool:
        if user == '':
            return True
        return bool(db.user.find('data', {'user': user}))

    @staticmethod
    def register_user(data):
        if data.get('pwd'):
            pwdmd5 = hashlib.md5(data['pwd'].encode(
                encoding='UTF-8')).hexdigest()
            data['pwd'] = pwdmd5
        data['photo'] = '/static/images/photo/' + \
            str(random.randint(1, 9))+'.jpg'
        data['lvl'] = 0
        data['exp'] = 0
        data['admin'] = 0
        data['titles'] = []
        data['pmodify'] = INITIAL_TIME
        data['last'] = INITIAL_TIME
        data['continuity'] = 0
        _uid = (db.user.find('data', sort=('_uid', -1), limit=1) or 100000)+1
        data['_uid'] = _uid
        db.user.insert('data', data)
