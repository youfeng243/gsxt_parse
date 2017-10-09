#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: find_field.py
@time: 2017/7/20 09:41
"""

import sys

sys.path.append('../')
from common.mongo import MongDb
from config.conf import mongo_db_webpage_new, mongo_db_webpage_old

from logger import Gsxtlogger

log = Gsxtlogger('find_field.log').get_logger()

target_db_new = MongDb(mongo_db_webpage_new['host'], mongo_db_webpage_new['port'], mongo_db_webpage_new['db'],
                       mongo_db_webpage_new['username'], mongo_db_webpage_new['password'], log=log)

target_db_old = MongDb(mongo_db_webpage_old['host'], mongo_db_webpage_old['port'], mongo_db_webpage_old['db'],
                       mongo_db_webpage_old['username'], mongo_db_webpage_old['password'], log=log)


def find_task(db, which):
    count = 0

    # 股权出质
    equity_pledged_info = u'equity_pledged_info'

    # 动产抵押登记信息
    chattel_mortgage_info = u'chattel_mortgage_info'

    source_table = "online_crawl_gansu_new"
    for item in db.traverse_batch(source_table):
        data_list = item.get('datalist')
        company = item.get('_id')

        count += 1

        if not isinstance(data_list, dict):
            log.error("{which} table: 没有 datalist company = {company}".format(
                company=company, which=which))
            continue

        for key, value in data_list.iteritems():
            if key == equity_pledged_info:
                if 'detail' in value:
                    log.info("{which} table: {equity} company = {company}".format(
                        equity=equity_pledged_info, company=company, which=which))
                continue

            if key == chattel_mortgage_info:
                if 'detail' in value:
                    log.info("{which} table: {chattel} company = {company}".format(
                        chattel=chattel_mortgage_info, company=company, which=which))
                continue

    log.info("查找结束: {which} count = {count}".format(which=which, count=count))


def main():
    find_task(target_db_new, 'new')
    find_task(target_db_old, 'old')


if __name__ == '__main__':
    main()
