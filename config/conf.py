# -*- coding:utf-8 -*-

# 新网页库
mongo_db_webpage_new = {
    "host": "172.17.1.119",
    "port": 40042,
    "db": "crawl_data",
    "username": 'work',
    "password": 'haizhi',
}
#
# mongo_db_webpage_new = {
#     "host": "172.16.215.2",
#     "port": 40042,
#     "db": "crawl_data_new",
#     "username": "work",
#     "password": "haizhi",
# }

# 旧网页库
mongo_db_webpage_old = {
    "host": "172.17.1.119",
    "port": 40042,
    "db": "crawl_data",
    "username": 'work',
    "password": 'haizhi',
}

company_data_source = {
    'host': "172.17.1.119",
    'port': 40042,
    'db': 'company_data',
    "username": 'work',
    "password": 'haizhi',
}


# 融合逻辑消息队列
merge_mq_conf = {
    'host': '172.17.1.120',
    'port': 11300,
    'tube': 'extract_info'
}

# 在线工商解析需要用到
parse_beanstalk_conf = {
    'host': 'cs0.sz-internal.haizhi.com', 'port': 11400,
    'tube': 'online_gsxt_parse'
}

