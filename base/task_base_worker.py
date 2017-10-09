#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence 
@file: task_base_worker.py
@time: 2016/12/7 16:17
"""
import os

from common.global_resource import global_log, is_debug, webpage_db_old, webpage_db_new, \
    company_data_db
from common.mongo import MongDb
from common.queue_mq_thread import MqQueueThread
from config.conf import merge_mq_conf


class TaskBaseWorker(object):
    #  -2 公司名称太短,
    # -1 公司名称不符合规格,
    # 0 代表抓取失败
    # 1 代表已经抓完了
    # 2 没有搜索到任何信息
    # 3 代表当前关键字搜索出列表结果 但是没有找到完整匹配关键字
    CRAWL_SHORT_NAME = -2
    CRAWL_INVALID_NAME = -1
    CRAWL_UN_FINISH = 0
    CRAWL_FINISH = 1
    CRAWL_NOTHING_FIND = 2
    CRAWL_NO_MATCH_NAME = 3

    # 从未成功
    NEVER_SUCCESS = -100

    # 过期时间
    RETENTION_TIME = 3600 * 24 * 7

    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 "
        "Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 "
        "Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    def __init__(self, **kwargs):

        # 获得项目根路径
        self.base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        # 初始化配置信息
        self.host = kwargs.get('host', '')
        self.logfile = kwargs.get('logfile', '')
        self.province = kwargs.get('province', '')
        self.target_table = kwargs.get('target_table', '')
        self.source_table = kwargs.get('source_table', '')
        self.crawl_flag = kwargs.get('crawl_flag', 'source_web')
        self.annual_table = kwargs.get('annual_table', None)
        self.gs_topic = int(kwargs.get('gs_topic', '49'))
        self.gs_nb_topic = int(kwargs.get('gs_nb_topic', '49'))
        self.is_nb_mq_open = eval(kwargs.get('is_nb_mq_open', 'False'))
        self.is_gs_mq_open = eval(kwargs.get('is_gs_mq_open', 'False'))

        self.never_success_flag = kwargs.get('never_success_flag', None)
        if self.never_success_flag is None:
            self.never_success_flag = self.NEVER_SUCCESS
        else:
            self.never_success_flag = int(self.never_success_flag)

        self.success_flag = kwargs.get('success_flag', None)
        if self.success_flag is None:
            self.success_flag = 1
        else:
            self.success_flag = int(self.success_flag)

        # 打开日志
        self.log = global_log

        # 搜索列表存储表
        self.webpage_db_old = webpage_db_old

        # 新的网页库表
        self.webpage_db_new = webpage_db_new

        # 种子库
        self.company_data_db = company_data_db

        # 目标库 存储数据到enterprise_gov_data
        self.target_db = webpage_db_new

        # 指向消息队列
        self.merge_mq = MqQueueThread(
            server_conf=merge_mq_conf, log=global_log)

        # 创建索引
        self.webpage_db_old.create_index(self.source_table, [(self.crawl_flag, MongDb.ASCENDING)])
        self.webpage_db_new.create_index(self.source_table, [(self.crawl_flag, MongDb.ASCENDING)])

        if is_debug is True:
            self.log.info('当前处于调试模式: is_debug = True')
        else:
            self.log.info('当前处于上线模式: is_debug = False')

    def query_company(self, company_name):
        pass

    def query_offline_task(self, item, choose_db_type):
        pass

    def query_online_task(self, company):
        pass
