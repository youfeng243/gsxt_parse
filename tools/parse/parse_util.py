#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: parse_util.py
@time: 2017/3/30 09:45
"""

# 列表类型
# 常规列表 表头和数据存在一个table里面
HORIZONTAL_LAYOUT = 0
# 双表结构, 第一个表存储表头 第二个表存储数据
DOUBLE_TABLE_LAYOUT = 1
# 多重表, 没有表头, key-value排布方式, 只需要解析数据即可
MULTI_VERTICAL_LAYOUT = 2

# 表格类型
# 表头
BLOCK_HEAD = 0
# 数据
BLOCK_DATA = 1


# 单元格信息
class Block(object):
    def __init__(self, value, block_type=BLOCK_DATA):
        self._value = value
        self._type = block_type

    def __str__(self):
        return str(self._value)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._value == other.value and self._type == other.type

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

# def main():
#     a = Block('1')
#     b = Block('1')
#     c = a
#     print a == b
#     print a
#     print b
#     print type(a)
#     print type(b)
#     print id(a)
#     print id(c)
#     print a == '1'
#
#
# if __name__ == '__main__':
#     main()
