#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: test_update.py
@time: 2017/7/26 22:32
"""

import sys

import time

sys.path.append('../')

from common.mongo import MongDb
from logger import Gsxtlogger

log = Gsxtlogger('test_update.log').get_logger()

company_data_source = {
    "host": "172.16.215.2",
    "port": 40042,
    "db": "company_data",
    "username": "work",
    "password": "haizhi",
}

company_data_db = MongDb(company_data_source['host'], company_data_source['port'], company_data_source['db'],
                         company_data_source['username'], company_data_source['password'], log=log)


def main():
    table = 'test_update'
    company_data_db.insert_batch_data(table, [{'_id': 'test',
                                               'key': '123456',
                                               'name': 'youfeng',
                                               'sex': 'man',
                                               }])
    time.sleep(5)
    company_data_db.insert_batch_data(table, [{
        '_id': 'test',
        'key': '59876',
        'name': 'lzz',
        'crawl_fix': 0,
    }])


if __name__ == '__main__':
    main()
