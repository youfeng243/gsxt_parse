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
from operator import itemgetter

from config.conf import mongo_db_webpage_new, mongo_db_webpage_old

sys.path.append('../')
from common.config_parser import ConfigParser
from common.mongo import MongDb
from logger import Gsxtlogger

# 开启日志
log = Gsxtlogger('never_success_total.log', for_mat='').get_logger()

target_db_new = MongDb(mongo_db_webpage_new['host'], mongo_db_webpage_new['port'], mongo_db_webpage_new['db'],
                       mongo_db_webpage_new['username'], mongo_db_webpage_new['password'], log=log)

target_db = MongDb(mongo_db_webpage_old['host'], mongo_db_webpage_old['port'], mongo_db_webpage_old['db'],
                   mongo_db_webpage_old['username'], mongo_db_webpage_old['password'], log=log)

province_py_to_zh = {
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


# 覆盖率
def count_never_success(config_list):
    log.info('省份        错误个数        总数      比例:')
    result_list = []
    for province, config_dict in config_list.iteritems():

        source_table = config_dict.get('source_table')
        if source_table is None:
            log.error('获取source_table失败')
            continue

        count_new = target_db_new.select_count(source_table, {'crawl_online': -100})
        total_new = target_db_new.select_count(source_table)
        count = target_db.select_count(source_table, {'crawl_online': -100})
        total = target_db.select_count(source_table)

        error_count = count + count_new
        total_count = total + total_new
        result_list.append((province, error_count, total_count, error_count * 100.0 / (total_count * 1.0)))

    result_list = sorted(result_list, key=itemgetter(3, 1), reverse=True)
    for result in result_list:
        log.info(u'{0:<15}{1:<10}{2:<15}{3}%'.format(province_py_to_zh[result[0]], result[1],
                                                     result[2], result[3]))
        # log.info('{province}    {error_count}   {total_count}   {p}%'.format(
        #     province=province_py_to_zh[province], error_count=count_new, total_count=total_new,
        #     p=(count_new * 100.0 / (total_new * 1.0))))
        # log.info('解析错误数目为: {error_count}'.format(error_count=count))
        # log.info('总数目为: {total_count}'.format(total_count=total))
        # log.info('解析错误比例: {p}%'.format(p=(count * 100.0 / (total * 1.0))))
        # log.info('')


        # 查看全部省份覆盖信息


def count_all():
    log.info('开始全量覆盖统计...')
    conf_parse = ConfigParser('../config/offline_gsxt_parse.conf')
    config_list = conf_parse.get_all_session()

    count_never_success(config_list)


def main():
    count_all()

    log.info('完成统计, 退出程序!')


if __name__ == '__main__':
    main()
