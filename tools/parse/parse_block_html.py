#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: parse_block_html.py
@time: 2017/3/28 11:31
"""
import json
import re
from Queue import Queue

from pyquery import PyQuery

from tools.parse.parse_block_base import BlockParser
from tools.parse.parse_util import HORIZONTAL_LAYOUT, MULTI_VERTICAL_LAYOUT, DOUBLE_TABLE_LAYOUT


class HTMLBlockParser(BlockParser):
    def __init__(self, content, field_map, log=None):
        """
        :param content: html 文本信息
        :param field_map: 属性字段
        """
        super(HTMLBlockParser, self).__init__()

        assert isinstance(content, basestring)
        assert isinstance(field_map, list)

        self.content = content.strip()
        if self.content == '':
            raise StandardError('content 不能为空字符串..')

        self.field_map = self.__unique_field(field_map)
        self.parse_result = dict()
        self.log = log

        # 存储所有table PyQuery
        self.root = PyQuery(self.content, parser='html')
        self.table_list = self.root.find('table')
        if self.table_list.length <= 0:
            return

        # 开始解析
        self.start_parse()

    @staticmethod
    def __unique_field(field_map):
        title_set = set()
        field_list = []
        for item in field_map:
            title = item.get('title')
            if title is None:
                continue
            if title in title_set:
                continue
            title_set.add(title)
            field_list.append(item)
        return field_list

    # 搜索html table
    def __search_html_list(self):
        html_fragment_list = list()

        for item in self.field_map:
            table_info = self.__search_table(item)
            if table_info is None:
                self.log.info('没有搜索到table信息: item = {item}'.format(
                    item=json.dumps(item, ensure_ascii=False)))
                continue
            html_fragment_list.append(table_info)

        return html_fragment_list

    # 在table_list中查找是否由表头信息
    def __find_table_in_list(self, title, layout):
        for table in self.table_list.items():
            if title not in table.text():
                continue

            if layout == HORIZONTAL_LAYOUT or layout == MULTI_VERTICAL_LAYOUT:
                return table.outer_html()

            if layout == DOUBLE_TABLE_LAYOUT:
                # self.log.info(table.outer_html())
                if table.next().length > 0:
                    temp_table = table.next()
                    if temp_table.is_('table'):
                        return table.outer_html() + temp_table.outer_html()

                    temp_table = temp_table.find('table')
                    if temp_table.length > 0:
                        return table.outer_html() + temp_table.outer_html()

                return None
            break

        return None

    # 找到下一个table
    @staticmethod
    def __find_next_table(element):

        iterator = element
        while True:
            temp = iterator.next()
            if temp.is_('table') and temp.length > 0:
                return temp

            find_table = temp.find('table')
            if find_table.length > 0:
                return temp

            if temp.length <= 0:
                return None

            iterator = temp

    # 查找文本完全匹配节点信息
    def __search_title_by_bfs(self, title):
        root = self.root
        search_title = title.strip()
        if search_title not in root.text():
            self.log.info('search_title = {title} 在html中没有出现过'.format(title=search_title))
            return None

        queue = Queue()
        queue.put(root)
        while not queue.empty():
            node = queue.get()
            if node.text().strip() == search_title:
                return node

            for item in node.children().items():
                if title in item.text():
                    queue.put(item)
        return None

    # 在html tree上查找table信息
    @staticmethod
    def __find_table_in_tree(layout, tree_node):

        table_num = 1
        if layout == DOUBLE_TABLE_LAYOUT:
            table_num = 2

        parent = tree_node.parent()
        while True:
            cur_table = 0
            result_html = ''

            def traverse_tree(total, node):

                html = ''
                current = 0
                table_list = node.find('table')
                for item in table_list.items():
                    html += item.outer_html()
                    current += 1
                    if current + total >= table_num:
                        return html, current
                return html, current

            temp_html, cur = traverse_tree(cur_table, tree_node)
            cur_table += cur
            result_html += temp_html
            if cur_table >= table_num:
                return result_html

            while tree_node.next().length > 0:
                tree_node = tree_node.next()

                temp_html, cur = traverse_tree(cur_table, tree_node)
                cur_table += cur
                result_html += temp_html
                if cur_table >= table_num:
                    return result_html

            if parent.length <= 0:
                break

            tree_node = parent
            parent = tree_node.parent()

        return None

    # 搜索table信息
    def __search_table(self, field_info):
        """
        根据title搜索相对应的table信息
        :param field_info: title相关信息
        :return: {title:xxx, layout:xxx, text:'html文本片段'}
        """
        assert 'title' in field_info
        assert 'layout' in field_info

        title = field_info.get('title')
        layout = field_info.get('layout')

        # 先判断整个页面中有没有对应的关键字
        if title not in self.content:
            return None

        table_info = dict(title=title, layout=layout)

        # 判断是否已经在单表中找到table
        html_text = self.__find_table_in_list(title, layout)
        if html_text is not None:
            table_info['text'] = html_text
            return table_info

        # 先查找title节点位置
        tree_node = self.__search_title_by_bfs(title)
        if tree_node is None:
            self.log.error('没有搜索到关键字节点信息: title = {title}'.format(title=title))
            return None

        html_text = self.__find_table_in_tree(layout, tree_node)
        if html_text is not None:
            table_info['text'] = html_text
            return table_info

        self.log.info('查找table失败: field_info = {field}'.format(field=field_info))
        return None

    def start_parse(self):
        """
        启动解析
        :return:
        """
        super(HTMLBlockParser, self).start_parse()

        # 根据field_map填充信息搜索table位置
        html_fragment_list = self.__search_html_list()

        for item in html_fragment_list:
            self.parse_result.update(self.parse_table(item))

    # 获得最大的列表宽度
    @staticmethod
    def __get_table_width(tr):
        width = 0

        # 遍历tr的子节点
        for child in tr.children().items():
            col_span = child.attr('colspan')
            width += int(col_span) if col_span is not None and col_span.strip() != '' else 1
            # self.log.info(child.text())
            # self.log.info(child.outer_html())

        return width

    # 获得行高
    @staticmethod
    def __get_table_heigth(tr):
        max_height = 1
        for child in tr.children().items():
            row_span = child.attr('rowspan')
            if row_span is None or row_span.strip() == '':
                continue

            max_height = int(row_span) if int(row_span) > max_height else max_height
        return max_height

    # 判断第一行是不是title
    @staticmethod
    def __has_title(tr_list):

        # 如果总共只有一行 则默认没有表名称信息
        if tr_list.length <= 1:
            return False

        width_list = []
        for tr_item in tr_list.items():
            width_list.append(tr_item.children().length)

        # 获得最大的列表宽度, 如果最大宽度都只有1 则默认没有title
        max_width = max(width_list)
        if max_width <= 1:
            return False

        if width_list[0] <= 1:
            return True

        return False

    @staticmethod
    def __find_next_block(table_list, row, width):

        col = 0
        while True:
            if col >= width:
                return -1
            if table_list[row][col] is None:
                return col

            col += 1

    # 开始解析表格信息
    def __parse_table(self, tr_list):

        # 计算最大高度
        max_height = 0

        # 获得最大的列表宽度
        max_width = 0
        for tr_item in tr_list.items():
            width = self.__get_table_width(tr_item)
            max_width = width if width > max_width else max_width
            max_height += self.__get_table_heigth(tr_item)

        max_width *= 2
        max_height *= 2

        # 先定义填充列表
        table_list = [[None for _ in xrange(max_width)] for _ in xrange(max_height)]

        # 记录当前填充的行信息
        cur_row = 0
        for tr_item in tr_list.items():
            for child in tr_item.children().items():
                row_span = child.attr('rowspan')
                if row_span is None or row_span.strip() == '':
                    row_span = 1
                else:
                    row_span = int(row_span)

                col_span = child.attr('colspan')
                if col_span is None or col_span.strip() == '':
                    col_span = 1
                else:
                    col_span = int(col_span)

                # 找到下一个可以填充的位置
                col = self.__find_next_block(table_list, cur_row, max_width)
                for c in xrange(col_span):
                    for r in xrange(row_span):
                        table_list[r + cur_row][c + col] = child.text().strip()

            cur_row += 1

        # 去除未填充的行列信息
        height_iter = max_height - 1
        while height_iter >= 0:
            width_iter = max_width - 1
            while width_iter >= 0:
                if table_list[height_iter][width_iter] is None:
                    del table_list[height_iter][width_iter]
                    width_iter -= 1
                    continue
                break
            if len(table_list[height_iter]) <= 0:
                del table_list[height_iter]
            height_iter -= 1

        # 填充为None的空格信息为空字符串
        max_height = len(table_list)
        height_iter = 0
        while height_iter < max_height:
            width_iter = 0
            max_width = len(table_list[height_iter])
            while width_iter < max_width:
                if table_list[height_iter][width_iter] is None:
                    self.log.info('发现未填充空格: x = {x} y = {y}'.format(x=height_iter, y=width_iter))
                    table_list[height_iter][width_iter] = ''
                width_iter += 1
            height_iter += 1

        # 输出表格信息
        for item_list in table_list:
            self.log.info(json.dumps(item_list, ensure_ascii=False))

        return table_list

    # 解析table {'title':'xxx', 'layout':xxx, 'text':'xxx'}
    def parse_table(self, field_info):
        result_dict = {}

        title = field_info.get('title')
        layout = field_info.get('layout')
        text = field_info.get('text')

        assert title is not None
        assert layout is not None
        assert text is not None
        assert text.strip() != ''

        # todo 去除html里面的注释文本 正则有多个解, 后期再做尝试, 先赶业务
        result_text = re.sub('<!--[\w\W\r\n]*?-->', '', text)
        if result_text is None or result_text.strip() == '':
            self.log.info('预处理后的字符串没有任何数据...result_text = {text}'.format(text=result_text))
            return result_dict

        tr_list = PyQuery(result_text, parser='html').find('tr')
        if tr_list.length <= 0:
            self.log.warn('title = {title} 没有任何tr数据,无法解析...'.format(title=title))
            self.log.warn('title = {title} table = {text}'.format(title=title, text=result_text))
            return result_dict

        # 判断第一行是不是表头名称
        if self.__has_title(tr_list):
            del tr_list[0]

        # 确定表头位置
        table_list = self.__parse_table(tr_list)
        result_dict[title] = table_list

        return result_dict

    # 解析title对应的table
    def get_block_values(self, title):
        """
        获得解析后的数据信息
        :param title: table 头部信息
        :return:
        """
        super(HTMLBlockParser, self).get_block_values(title)
        return self.parse_result.get(title, [])

    # 合并翻页数据
    @staticmethod
    def merge_table(first_list, second_list):
        """
        合并二维数组数据, 需要去掉表头信息进行合并
        :param first_list: 需要合并的数据
        :param second_list: 需要合并的数据
        :return:
        """
        assert isinstance(first_list, list)
        assert isinstance(second_list, list)

        first_len = len(first_list)
        second_len = len(second_list)
        min_len = min(first_len, second_len)

        count = 0
        while count < min_len:
            assert isinstance(first_list[count], list)
            assert isinstance(second_list[count], list)
            temp_first_len = len(first_list[count])
            temp_second_len = len(second_list[count])
            if temp_first_len != temp_second_len:
                break

            is_equal = True
            for index in xrange(temp_first_len):
                if first_list[count][index] != second_list[count][index]:
                    is_equal = False
                    break

            if not is_equal:
                break

            count += 1

        for index in xrange(count, second_len):
            first_list.append(second_list[index])

        return first_list
