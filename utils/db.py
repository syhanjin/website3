# -*- coding: utf-8 -*-
import datetime
import random
from typing import Any
import pymongo
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, InsertManyResult, InsertOneResult, UpdateResult
from utils import datas
import utils

from utils.typing import DICT


class Db(object):
    def __init__(self, name: str):
        self.name = name
        client = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = client[name]

    def insert(self, collection: str, data: 'dict | list') -> 'InsertOneResult | InsertManyResult':
        """
        向指定集合插入内容
        :param collection: 集合名
        :param data: 数据
        """
        if type(data) == DICT:
            return self.db[collection].insert_one(data)
        else:
            return self.db[collection].insert_many(list(data))

    def update(self, collection: str, filter, update, upsert=False, type: int = 0) -> UpdateResult:
        """
        升级条目
        :param collection: 集合名
        :param filter: A query that matches the document to update.
        :param update: The modifications to apply.
        :param upsert (optional): If True, perform an insert if no documents match the filter.
        :param type: 0 | 1 为0则处理一条， 为1则处理多条
        """
        if type == 0:
            return self.db[collection].update_one(filter, update, upsert)
        elif type == 1:
            return self.db[collection].update_many(filter, update, upsert)

    def delete(self, collection: str, filter, type: int = 0) -> DeleteResult:
        """
        删除条目
        :param collection: 集合名
        :param filter: A query that matches the document to update.
        :param type: 0 | 1 为0处理一条， 为1则处理多条
        """
        if type == 0:
            return self.db[collection].delete_one(filter)
        elif type == 1:
            return self.db[collection].delete_many(filter)

    def find(
        self,
        collection: str,
        filter=None,
        type: int = 0,
        skip: 'int | None' = None,
        limit: 'int | None' = None,
        sort: 'tuple[str, int] | None' = None,
        origin: bool = False,
    ) -> 'dict | list | Cursor':
        """
        查找条目
        :param collection: 集合名
        :param filter: A query that matches the document to update.
        :param type: 0 | 1 为0处理一条， 为1则处理多条
        :param skip: 跳过的条数
        :param limit: 返回条数限制
        :param sort: (key, direction) 排序条目
        :param origin: 为True 返回未列表化的数据
        """
        if type == 0:
            data = self.db[collection].find_one(filter)
            if data is not None:
                data['_id'] = str(data['_id'])
            return data

        elif type == 1:
            data = self.db[collection].find(filter)
            if sort is not None:
                data = data.sort(*sort)
            if skip is not None:
                data = data.skip(skip)
            if limit is not None:
                data = data.limit(limit)
            if origin:
                return data
            data = list(data)
            for i in data:
                i['_id'] = str(i['_id'])
            return data

    def find_page(self, collection: str, filter, page: int, size: int):
        """
        查找第几页条目
        :param collection: 集合名
        :param filter: A query that matches the document to update.
        :param page: 页数
        :param size: 每页大小
        """
        return self.find(collection, filter, 1, (page - 1) * size, size)

    def create_kv_pairs(
        self,
        collection: str,
        value: str,
        survival_time: datetime.timedelta
    ) -> str:
        key = datas.make_key()
        self.db[collection].insert_one({
            'key': key,
            'value': value,
            'deadline': datetime.datetime.now() + survival_time
        })
        return key

    def get_kv_pairs(
        self,
        collection: str,
        key: str,
        delete: bool = True
    ) -> Any:
        data = self.db[collection].find_one({'key': key})
        if data is None:
            return None
        dead = data['deadline'] < datetime.datetime.now()
        if delete or dead:
            self.db[collection].delete_one({'_id': data['_id']})
        if dead:
            return None
        return data['value']

    def has_kv_pairs(
        self,
        collection: str,
        key: str,
    ):
        data = self.db[collection].find_one({'key': key})
        if data is None:
            return False
        dead = data['deadline'] < datetime.datetime.now()
        if dead:
            self.db[collection].delete_one({'_id': data['_id']})
            return False
        return True


user = Db('user')
main = Db('main')
