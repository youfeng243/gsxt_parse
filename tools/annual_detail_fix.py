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

from common.global_field import Model

sys.path.append('../')

from common.mongo import MongDb
from logger import Gsxtlogger

log = Gsxtlogger('search_no_datalist.log').get_logger()

province_map = {
    'shanghai': '上海',
    'yunnan': '云南',
    'neimenggu': '内蒙古',
    'beijing': '北京',
    'jilin': '吉林',
    'sichuan': '四川',
    'tianjin': '天津',
    'ningxia': '宁夏',
    'anhui': '安徽',
    'shandong': '山东',
    'shanxicu': '山西',
    'guangdong': '广东',
    'guangxi': '广西',
    'xinjiang': '新疆',
    'jiangsu': '江苏',
    'jiangxi': '江西',
    'hebei': '河北',
    'henan': '河南',
    'zhejiang': '浙江',
    'hainan': '海南',
    'hubei': '湖北',
    'hunan': '湖南',
    'gansu': '甘肃',
    'fujian': '福建',
    'xizang': '西藏',
    'guizhou': '贵州',
    'liaoning': '辽宁',
    'chongqing': '重庆',
    'shanxi': '陕西',
    'qinghai': '青海',
    'heilongjiang': '黑龙江',
    'gsxt': '总局',
}

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


def fix_annual_detail(province):
    count = 0
    log.info('province = {province}'.format(province=province))
    source_table = 'online_crawl_{province}_new'.format(province=province)
    log.info('source_table = {source_table}'.format(source_table=source_table))

    target_table_cursor = target_db.db[source_table].find({'crawl_online': -100},
                                                          no_cursor_timeout=True).batch_size(
        10000)

    for item in target_table_cursor:
        try:
            count += 1
            data_list = item.get('datalist')
            company = item.get('_id')
            if data_list is None:
                log.error('company = {company} 没有datalist'.format(company=company))
                continue

            annual = data_list.get('annual_info')
            if annual is None:
                log.error('company = {company} 没有年报信息'.format(company=company))
                continue

            if Model.type_detail in annual:
                continue

            if Model.type_list not in annual:
                data_list.pop('annual_info')
                target_db.insert_batch_data(source_table, [item])
                continue

            table_list = annual.get(Model.type_list)
            annual[Model.type_detail] = table_list
            annual.pop(Model.type_list)
            target_db.insert_batch_data(source_table, [item])
            log.info('当前进度: count = {count}'.format(count=count))
        except Exception as e:
            log.exception(e)

    target_table_cursor.close()


def main():
    log.info('开始清洗数据')

    province = 'chongqing'
    if len(sys.argv) > 1:
        province = sys.argv[1]

    fix_annual_detail(province)

    log.info('清洗数据完成, 退出程序')


if __name__ == '__main__':
    main()
