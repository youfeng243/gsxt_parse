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

from common.mongo import MongDb
from logger import Gsxtlogger

log = Gsxtlogger('delete_messy_code_data.log').get_logger()

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

target_db = MongDb(crawl_data_source['host'], crawl_data_source['port'], crawl_data_source['db'],
                   crawl_data_source['username'], crawl_data_source['password'], log=log)

webpage_db_old = MongDb(company_data_source['host'], company_data_source['port'], company_data_source['db'],
                   company_data_source['username'], company_data_source['password'], log=log)


def main():
    count = 0
    log.info('开始清洗数据')

    province = 'hunan'
    if len(sys.argv) > 1:
        province = sys.argv[1]

    log.info('province = {province}'.format(province=province))
    source_table = 'online_crawl_{province}_new'.format(province=province)
    log.info('source_table = {source_table}'.format(source_table=source_table))

    search_table = 'online_all_search'
    list_table = 'offline_all_list'

    target_table_cursor = target_db.db[source_table].find({'crawl_online': -100},
                                                          no_cursor_timeout=True).batch_size(
        10000)

    for item in target_table_cursor:
        try:
            count += 1
            _id = item.get('_id')
            search_name = item.get('search_name')
            company_name = item.get('seed')
            if search_name is None:
                log.info('search_name is None: _id = {_id}'.format(_id=_id))
                continue

            if company_name is None:
                log.info('company_name is None: _id = {_id}'.format(_id=_id))
                continue

            log.info('_id = {_id}'.format(_id=_id))
            log.info('search_name = {search_name}'.format(search_name=search_name))
            log.info('seed = {seed}'.format(seed=company_name))

            result_item = webpage_db_old.find_one(search_table, {'search_name': search_name})
            if result_item is not None:
                result_item['crawl_online'] = 0
                webpage_db_old.save(search_table, result_item)
                log.info('save search_table success {com}'.format(com=search_name))

            result_item = webpage_db_old.find_one(list_table, {'company_name': company_name})
            if result_item is not None:
                result_item['crawl_online'] = 0
                webpage_db_old.save(list_table, result_item)
                log.info('save list_table success {com}'.format(com=company_name))

            target_db.delete(source_table, _id)
            log.info('当前进度: count = {count}'.format(count=count))
        except Exception as e:
            log.exception(e)

    target_table_cursor.close()

    log.info('清洗数据完成, 退出程序')


if __name__ == '__main__':
    main()
