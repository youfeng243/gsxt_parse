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

from common import util
from common.mongo import MongDb
from logger import Gsxtlogger

log = Gsxtlogger(util.get_pid_log_name('copy_offline_all_list_by_file.py')).get_logger()

count = 0

mongo_db_crawl_data = {
    'host': '172.16.215.2',
    'port': 40042,
    'db': 'company_data',
    'username': 'work',
    'password': 'haizhi'
}

webpage_db_old = MongDb(mongo_db_crawl_data['host'], mongo_db_crawl_data['port'], mongo_db_crawl_data['db'],
                   mongo_db_crawl_data['username'], mongo_db_crawl_data['password'], log=log)


def main():
    log.info('开始读取数据发送到kafka..')
    source_table = 'offline_all_list'
    province = 'gsxt'
    with open('import_company') as pfile:
        batch_list = []
        cnt = 0
        for line in pfile:
            company = line.strip()
            log.info(company)
            data = {
                '_id': util.generator_id({}, company, province),
                'company_name': company,
                'province': province,
                'in_time': util.get_now_time(),
            }
            batch_list.append(data)
            cnt += 1
            if cnt >= 10000:
                webpage_db_old.insert_batch_data(source_table, batch_list)
                del batch_list[:]
                cnt = 0
                log.info('插入数据')
        if len(batch_list) > 0:
            webpage_db_old.insert_batch_data(source_table, batch_list)
            log.info('插入最后数据')

    log.info('退出程序')


if __name__ == '__main__':
    main()
