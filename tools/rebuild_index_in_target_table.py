#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence 
@file: test_mongodb_result_total.py
@time: 2016/12/9 22:22
"""
import sys
import threading
import time

sys.path.append('../')
from common.config_parser import ConfigParser
from config.conf import mongo_db_target
from common.mongo import MongDb
from logger import Gsxtlogger

# 开启日志
log = Gsxtlogger('rebuild_index_in_target_table.log').get_logger()

target_db = MongDb(mongo_db_target['host'], mongo_db_target['port'], mongo_db_target['db'],
                   mongo_db_target['username'], mongo_db_target['password'], log=log)


def func(source_table, province):
    log.info('start: province = {province}'.format(province=province))
    target_db.create_index(source_table, [('first_120', MongDb.ASCENDING)])
    log.info('finish: province = {province}'.format(province=province))


def rebuild_index(config_list):
    start_time = time.time()

    thread_list = []
    for key, value in config_list.iteritems():
        source_table = value.get('source_table', None)
        if source_table is None:
            log.error('读取表信息错误')
            continue

        province = value.get('province', '')
        thread = threading.Thread(target=func, args=(source_table, province))
        thread.start()
        thread_list.append(thread)

    log.info('go to join')
    for thread in thread_list:
        thread.join()

    end_time = time.time()

    log.info('')
    log.info('start_time: {start}'.format(start=start_time))
    log.info('end_time: {end}'.format(end=end_time))
    log.info('used = {used}s'.format(used=(end_time - start_time)))
    log.info('')


def total_target(value=None, config_list=None):
    start_time = time.time()
    count = 0

    value = {'rank': {'$ne': None}} if value is None else value
    log.info('开始统计抓取结果: {value}'.format(value=value))

    for key, v in config_list.iteritems():
        target_table = v.get('target_table', None)
        if target_table is None:
            log.error('读取表信息错误')
            continue
        log.info('table = {table}'.format(table=target_table))
        result = target_db.select_count(target_table, value)
        count += result

        log.info('result {province}: size = {size}'.format(province=key, size=result))

    log.info('总抓取量为: size = {size}'.format(size=count))
    end_time = time.time()

    log.info('start_time: {start}'.format(start=start_time))
    log.info('end_time: {end}'.format(end=end_time))
    log.info('used = {used}s'.format(used=(end_time - start_time)))
    log.info('')


def main():
    config = 'offline_gsxt_parse.conf'
    if len(sys.argv) > 1:
        config = sys.argv[1]
    # conf_parse = ConfigParser('../config/cmb_gsxt_detail.conf')
    conf_parse = ConfigParser('../config/' + config)
    config_list = conf_parse.get_all_session()

    rebuild_index(config_list)


if __name__ == '__main__':
    main()
