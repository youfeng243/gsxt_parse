#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: kafka_producer.py
@time: 2016/12/19 16:32
"""
import sys

sys.path.append('../')
from common.global_field import Model
from common.mongo import MongDb
from logger import Gsxtlogger

log = Gsxtlogger('fix_annual_shandong.log').get_logger()

company_data_source = {
    "host": "172.16.215.2",
    "port": 40042,
    "db": "company_data",
    "username": "work",
    "password": "haizhi",
}

crawl_data_source = {
    "host": "172.16.215.2",
    "port": 40042,
    "db": "crawl_data",
    "username": "offline",
    "password": "offline",
}

# 新网页库
mongo_db_webpage_new = {
    "host": "172.16.215.2",
    "port": 40042,
    "db": "crawl_data_new",
    "username": "work",
    "password": "haizhi",
}

target_db = MongDb(crawl_data_source['host'], crawl_data_source['port'], crawl_data_source['db'],
                   crawl_data_source['username'], crawl_data_source['password'], log=log)

target_db_new = MongDb(mongo_db_webpage_new['host'], mongo_db_webpage_new['port'], mongo_db_webpage_new['db'],
                       mongo_db_webpage_new['username'], mongo_db_webpage_new['password'], log=log)

webpage_db_old = MongDb(company_data_source['host'], company_data_source['port'], company_data_source['db'],
                   company_data_source['username'], company_data_source['password'], log=log)


def fix_annual(database_db):
    count = 0
    province = 'shandong'
    log.info('province = {province}'.format(province=province))
    source_table = 'online_crawl_{province}_new'.format(province=province)
    log.info('source_table = {source_table}'.format(source_table=source_table))

    target_table_cursor = database_db.db[source_table].find({}, no_cursor_timeout=True).batch_size(500)
    result_list = []
    length = 0
    for item in target_table_cursor:
        try:
            count += 1
            data_list = item.get('datalist')
            if data_list is None:
                continue

            annual_info = data_list.get(Model.annual_info)
            if annual_info is None:
                continue

            if Model.type_detail in annual_info:
                continue

            crawl_online = item.get('crawl_online')
            if crawl_online == -100:
                item['crawl_online'] = 0

            data_list.pop(Model.annual_info)

            # database_db.insert_batch_data(source_table, [item])
            length += 1
            result_list.append(item)
            if length >= 500:
                database_db.insert_batch_data(source_table, result_list)
                del result_list[:]
                length = 0

            log.info('当前进度: count = {count}'.format(count=count))
        except Exception as e:
            log.exception(e)

    database_db.insert_batch_data(source_table, result_list)
    target_table_cursor.close()


def main():
    log.info('开始清洗数据')

    fix_annual(target_db)
    fix_annual(target_db_new)

    log.info('清洗数据完成, 退出程序')


if __name__ == '__main__':
    main()
