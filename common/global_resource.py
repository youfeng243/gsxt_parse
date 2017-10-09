# coding=utf-8
import sys

from common.mongo import MongDb
from config.conf import mongo_db_webpage_old, mongo_db_webpage_new, company_data_source
from logger import Gsxtlogger

CHOOSE_DB_OLD = 0
CHOOSE_DB_NEW = 1

length = len(sys.argv)
# 判断是否是在debug模式下
if length > 0:
    is_debug = False
else:
    is_debug = True

# 判断是否可以通过省份进行区分log
if length > 3:
    log_name = 'start_parse_task_' + sys.argv[2] + '.log'
else:
    log_name = 'start_parse_task.log'

global_logger = Gsxtlogger(log_name)
global_log = global_logger.get_logger()

# 新网页库
webpage_db_new = MongDb(mongo_db_webpage_new['host'], mongo_db_webpage_new['port'], mongo_db_webpage_new['db'],
                        mongo_db_webpage_new['username'],
                        mongo_db_webpage_new['password'], log=global_log)

# 旧网页库
webpage_db_old = MongDb(mongo_db_webpage_old['host'], mongo_db_webpage_old['port'], mongo_db_webpage_old['db'],
                        mongo_db_webpage_old['username'],
                        mongo_db_webpage_old['password'], log=global_log)

company_data_db = MongDb(company_data_source['host'], company_data_source['port'], company_data_source['db'],
                         company_data_source['username'], company_data_source['password'], log=global_log)
