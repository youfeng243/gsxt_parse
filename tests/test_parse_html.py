#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: test_parse_html.py
@time: 2017/3/28 11:45
"""
from unittest import TestCase

from logger import Gsxtlogger
from tools.parse import parse_util
from tools.parse.parse_block_html import HTMLBlockParser

global_logger = Gsxtlogger('tests.log')
global_log = global_logger.get_logger()


class TestParseHtml(TestCase):
    @staticmethod
    def read_file(path):
        with open(path) as p_file:
            return p_file.read().decode(encoding='utf-8')

    def setUp(self):
        print 'init by setUp...'

    def tearDown(self):
        print 'end by tearDown...'

    # 单表测试
    def test_tianjin_credit(self):
        content = self.read_file('天津测试.txt')
        field_map = list()
        # [{'title':'xxx', 'selector':'xxx', 'layout':xxx}]
        field_map.append({'title': "基本信息", 'layout': parse_util.MULTI_VERTICAL_LAYOUT})
        field_map.append({'title': "股东信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "变更信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "主要人员信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "分支机构信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "清算信息", 'layout': parse_util.MULTI_VERTICAL_LAYOUT})
        field_map.append({'title': "动产抵押登记信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "股权出质登记信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "行政处罚信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "经营异常信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "严重违法信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "抽查检查信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "企业年报", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "变更信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "股东及出资信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "股权变更信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "行政许可信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "知识产权出质登记信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "行政处罚信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "行政许可信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "参加经营的家庭成员姓名", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "司法股权冻结信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "司法股东变更登记信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        field_map.append({'title': "年报信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        html_parse = HTMLBlockParser(content, field_map=field_map, log=global_log)

        # content_cells = html_parse.get_block_values('主要人员信息')
        # self.assertEquals("序号", content_cells[0][0])
        # self.assertEquals("高峰", content_cells[1][1])
        # self.assertEquals("2", content_cells[2][0])
        # self.assertEquals("4", content_cells[4][0])
        # self.assertEquals("张祖刚", content_cells[5][1])
        # self.assertEquals("郝彤", content_cells[10][1])

        content_cells = html_parse.get_block_values("主要人员信息")

        content_cells = html_parse.get_block_values('清算信息')
        # self.assertEquals("登记机关", content_cells[0][3])
        # self.assertEquals("天津南环铁路有限公司黄万运管分公司", content_cells[1][2])
        # self.assertEquals("2", content_cells[2][0])
        # self.assertEquals("120224000057610", content_cells[2][1])

    # 双表测试
    def test_guangxi_credit(self):
        content = self.read_file('广西测试.txt')
        field_map = list()
        field_map.append({'title': "基本信息", 'layout': parse_util.MULTI_VERTICAL_LAYOUT})
        field_map.append({'title': "股东信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "变更信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "主要人员信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "分支机构信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "清算信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "动产抵押登记信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "股权出质登记信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "行政处罚信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "经营异常信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "严重违法信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "抽查检查信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "企业年报", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "变更信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "股东及出资信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "股权变更信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "行政许可信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "知识产权出质登记信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "行政处罚信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "行政许可信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "参加经营的家庭成员姓名", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "司法股权冻结信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "司法股东变更登记信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        field_map.append({'title': "年报信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})

        html_parse = HTMLBlockParser(content, field_map=field_map, log=global_log)

        content_cells = html_parse.get_block_values("基本信息")
        # self.assertEquals("宁明县工商行政管理局", content_cells[1][5])
        # self.assertEquals("营业期限自", content_cells[0][3])
        # self.assertEquals("2050年12月26日", content_cells[1][9])
        # self.assertEquals("存续", content_cells[1][11])
        # self.assertEquals("成立日期", content_cells[0][6])
        # self.assertEquals("登记状态", content_cells[0][11])

        content_cells = html_parse.get_block_values("变更信息")
        self.assertEquals("2014年7月9日", content_cells[1][3])
        self.assertEquals("变更前内容", content_cells[0][1])
        self.assertEquals("经营范围", content_cells[1][0])

        content_cells = html_parse.get_block_values("抽查检查信息")
        self.assertEquals("序号", content_cells[0][0])
        self.assertEquals("2015年11月6日", content_cells[1][3])
        self.assertEquals("日期", content_cells[0][3])

        # 双表测试
        # def test_heilongjiang_credit(self):
        #     content = self.read_file('黑龙江测试.txt')
        #     field_map = list()
        #     field_map.append({'title': "营业执照信息", 'layout': parse_util.MULTI_VERTICAL_LAYOUT})
        #     field_map.append({'title': "股东及出资信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "变更信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     # field_map.append({'title': "主要人员信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     # field_map.append({'title': "分支机构信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     # field_map.append({'title': "清算信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "动产抵押登记信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "股权出质登记信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     # field_map.append({'title': "行政处罚信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "经营异常信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "严重违法信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "抽查检查信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "企业年报信息", 'layout': parse_util.HORIZONTAL_LAYOUT})
        #     # field_map.append({'title': "变更信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     # field_map.append({'title': "股东及出资信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "股权变更信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     # field_map.append({'title': "行政许可信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "知识产权出质登记信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     # field_map.append({'title': "行政处罚信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     # field_map.append({'title': "行政许可信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "参加经营的家庭成员姓名", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "司法股权冻结信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "司法股东变更登记信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #     field_map.append({'title': "年报信息", 'layout': parse_util.DOUBLE_TABLE_LAYOUT})
        #
        #     html_parse = HTMLBlockParser(content, field_map=field_map, log=global_log)
