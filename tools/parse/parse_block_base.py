#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: parse_block_base.py
@time: 2017/3/28 11:22
"""


class BlockParser(object):
    def __init__(self):
        """
        :param page_list: 页面信息 [xxx, xxx]
        :param field_map: 需要提取的属性 [{'title':'xxx', 'selector':'xxx', 'layout':xxx}]
        title: 选填, 标题名称, 解析后根据标题名称提取数据, 如果没有填title则根据下表数字进行表格数据提取_num
        selector: 选填, 对于特殊表格需要selector才能够解析则必填, 如果设置了selector 优先使用这个属性进行提取解析
        layout: 必填, 根据这个属性确定表格特征, 且解析后返回数据也根据这个属性不同而不同
        """
        pass

    def get_block_values(self, title_key):
        pass

    def start_parse(self):
        pass
