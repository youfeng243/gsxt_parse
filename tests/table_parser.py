#!/usr/bin/python
# coding:utf-8
import itertools
import json
import re
import sys
from xml.etree import ElementTree as etree

import numpy as np
from BeautifulSoup import BeautifulSoup as bs
from key_check import KEYChecker
from lxml.html import clean

reload(sys)
sys.setdefaultencoding('utf-8')

sys.setrecursionlimit(1000)

DEBUG = False


# DEBUG = True


def accumulate(iterator):
    total = 0
    for item in iterator:
        total += item
        yield total


def similarity(a, b):
    aa = set(a)
    bb = set(b)
    return len(aa & bb) * 1.0 / len(aa | bb)
    # return SequenceMatcher(None, a, b).ratio()


# http://www.8yu.cn/ZhaoBiao/2942340.html
def check_colon_table(line):
    line = [_.replace(':', '：') for _ in line]
    colon_in = [u'：' in _ for _ in line]
    colon_last = [_.endswith(u'：') for _ in line]
    if len(line) >= 2 and all(colon_in[1:]) and not all(colon_last[1:]):
        return True
    else:
        return False


class HTMLTableParser():
    def __init__(self, keyword_path):
        self.cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset(
            ['colspan', 'rowspan', 'height', 'width']))  # , 'href', 'onclick'

        self.key_checker = KEYChecker('./keys.txt')

        self.turning_points = [u'投诉电话', u'监管部门', u'监管部门', u'监督部门', u'监理机构', u'建设单位', u'代建单位', u'招标人', u'中标人', u'招标单位',
                               u'代理机构', u'代理人', u'代理单位', u'代理', u'乙方', u'序号', u'候选人', u'中标范围']

        self.re_colon = re.compile(u'（[^>]*?）')

    def key_scores(self, rows):
        lst_str = []
        lst_num = []
        for line in rows:
            # lst_str.append([str(self.key_checker.score(item)) for item in line])
            ss = [self.key_checker.score(item) for item in line]
            lst_num.append(ss)
            lst_str.append([str(x) for x in ss])
        return lst_str, lst_num

    def get_col(self, rows, j):
        col = []
        for line in rows:
            col.append(line[j])
        return col

    def drop_null_cols(self, rows):
        colnums = [len(x) for x in rows]
        if len(set(colnums)) != 1:
            return rows
        width = colnums[0]
        if width < 2:
            return rows
        first_colum = self.get_col(rows, 0)
        if re.sub(u'[\d,\.\s，、一二三四五六七八九十☒]+', '', u''.join(first_colum)) == u'':
            for l in xrange(len(rows)):
                rows[l] = [rows[l][0].replace(u'☒', '') + '' + rows[l][1]] + rows[l][2:]
            width -= 1
        ct = 0
        for i in xrange(width):
            col = self.get_col(rows, ct)
            if len(set(col)) == 1 and (col[0] == u'☒' or col[0] == ''):
                for line in rows:
                    del line[ct]
            else:
                ct += 1
        return rows

    def drop_null_cols_scores(self, rows, scores, width):
        colnums = [len(x) for x in rows]
        if len(set(colnums)) != 1:
            return rows
        width = colnums[0]
        ct = 0
        for i in xrange(width):
            col = self.get_col(rows, ct)
            if len(set(col)) == 1 and (col[0] == u'☒' or col[0] == ''):
                for j in xrange(len(rows)):
                    del rows[j][ct]
                    # del scores[j][ct]
                    width -= 1
                np.delete(scores, ct, 1)
            else:
                ct += 1
        return rows, scores, width

    '''
    def normalize_key():
        tmp = rows[i][1].replace('(', u'（').replace(':', u'（').replace(u'：', u'（').replace(u'名称', u'（')
        tmp = tmp.strip()
        if emp.endswith(u'名称'):
            tmp = tmp[:-2]
        tmp = tmp.strip()
        if emp.endswith(u':') or emp.endswith(u'：'):
            tmp = tmp[:-1]
        tmp = tmp.split(u'（')[0]
        return tmp
    '''

    def v2kv(self, x):

        beside_colon = x
        beside_colon = re.sub(u'\w：\w', '', beside_colon)
        x = x.replace('(', u'（').replace(')', u'）')
        if x.count(u'（') == 1 and x.count(u'）') == 1:
            beside_colon = re.sub(self.re_colon, '', x)
        if beside_colon.count(u'：') == 1 and x.split(u'：')[1].strip() != '' and self.key_checker.score(
                x.split(u'：')[0]) > 0.4:
            return {x.split(u'：')[0]: u'：'.join(x.split(u'：')[1:])}
        else:
            return [x]

    def recursive_parse(self, parsed_previous, rows_remained, scores_remained):
        parsed_remained = self.parse_kv(rows_remained, scores_remained)
        # assert(isinstance(parsed_previous, list))
        if isinstance(parsed_remained, list):
            return parsed_previous + parsed_remained
        elif isinstance(parsed_remained, dict):
            return parsed_previous + [parsed_remained, ]
        else:
            return parsed_previous

    def parse_kv_matrix(self, rows, scores, width):
        rows, scores, width = self.drop_null_cols_scores(rows, scores, width)
        scores = np.array(scores)
        parsed_dict = []
        merge_cell = u'→' in self.get_col(rows, 0)
        # print '\t'.join(self.get_col(rows,0)[1:])
        if not merge_cell and len(rows) > 2 and width > 2 and scores[:, 0].mean() > 0.7 and (
                np.max(np.mean(scores[:, 1:], axis=0)) < 0.35 or (
                np.max(np.mean(scores[1:, 1:], axis=0)) < 0.35 and len(
                set.intersection(*[set(x.replace(u'：', '').strip()) for x in rows[0][1:]])) > 0)) and len(
                set.intersection(*[set(x.replace(u'：', '').strip()) for x in self.get_col(rows, 0)[1:]])) == 0:
            for i in xrange(1, width):
                dd = {}
                for j in xrange(len(rows)):
                    dd[rows[j][0]] = rows[j][i]
                parsed_dict.append(dd)
            parsed_dict = [parsed_dict]

        elif not merge_cell and len(rows) == 1:
            parsed_dict = {}
            if width % 2 == 0:
                if scores[0][::2].mean() > 0.6 and scores[0][1::2].mean() < 0.4 and not (
                        u'：' in rows[0][0][:-1] and u'：' in rows[0][1][:-1]):
                    for i in xrange(0, len(rows[0]), 2):
                        parsed_dict[rows[0][i]] = rows[0][i + 1]
                    return parsed_dict
                elif all([(u'：' in x) for x in rows[0]]) and all(
                        [(self.key_checker.score(x.split(u'：')[1]) < 0.5) for x in rows[0]]):
                    parsed_dict = {}
                    for x in rows[0]:
                        parsed_dict[x.split(u'：')[0].strip()] = u'：'.join(x.split(u'：')[1:])
                else:
                    return [rows[0], ]
            else:
                return [rows[0], ]

        elif not merge_cell and width == 2:
            ul = scores[0][0]
            bl = scores[1][0]
            ur = scores[0][1]
            if u'：' in rows[0][0][:-1] and u'：' in rows[0][1][:-1]:
                parall = 0
                for i in xrange(len(rows)):
                    line = rows[i]
                    l1 = ''
                    l2 = ''
                    if u'：' not in line[0] or u'：' not in line[1]:
                        break
                    l1 = line[0].split(u'：')[0]
                    l2 = line[1].split(u'：')[0]
                    if l1 == l2:
                        parall += 1
                if parall >= 2:  # and u'：' in rows[0][0] and u'：' in rows[0][1]:
                    h1 = rows[0][0].split(u'：')[0]
                    h2 = rows[0][1].split(u'：')[0]
                    d1 = {}
                    d2 = {}
                    for i in xrange(len(rows)):
                        if u'：' in rows[0][0] and u'：' in rows[0][1]:
                            line = rows[i]
                            l1 = ''
                            r1 = line[0]
                            l2 = ''
                            if u'：' in line[0]:
                                l1 = line[0].split(u'：')[0]
                                r1 = u'：'.join(line[0].split(u'：')[1:])
                                d1[l1] = r1
                            if u'：' in line[1]:
                                l2 = line[1].split(u'：')[0]
                                r2 = u'：'.join(line[1].split(u'：')[1:])
                                d2[l2] = r2
                        else:
                            return self.recursive_parse([d1, d2], rows[i:], scores[i:])
                    parsed_dict = [d1, d2]
                else:
                    parsed_dict = []
                    i = 0
                    for i in xrange(len(rows)):
                        if u'：' in rows[i][0] and u'：' in rows[i][1]:
                            dd = {}
                            dd[rows[0][0].split(u'：')[0]] = u'：'.join(rows[0][0].split(u'：')[1:])
                            dd[rows[0][1].split(u'：')[0]] = u'：'.join(rows[0][1].split(u'：')[1:])
                            parsed_dict.append(dd)
                        else:
                            return self.recursive_parse(parsed_dict, rows[i:], scores[i:])
            elif scores[:, 0].mean() > 0.65 and scores[:, 1].mean() < 0.35 and len(set(self.get_col(rows, 0))) == len(
                    rows):  # ul>=0.6 and bl>=0.6 and ur<0.5:
                parsed_dict = {}
                for i in xrange(len(rows)):
                    tmp = rows[i][0].replace(u'：', '')
                    if (tmp in parsed_dict or any([tmp.endswith(x) for x in self.turning_points])) and i != 0:
                        return self.recursive_parse([parsed_dict, ], rows[i:], scores[i:])
                    else:
                        parsed_dict[rows[i][0].replace(u'：', '')] = rows[i][1]
            elif ul >= 0.6 and ur >= 0.56 and scores[1:, :].mean() < 0.4 and rows[0][0] != rows[0][1]:
                h1 = rows[0][0].replace(u'：', '')
                h2 = rows[0][1].replace(u'：', '')
                parsed_dict = []
                for i in xrange(1, len(rows)):
                    if scores[i, :].min() > 0.7:
                        # print rows[i][0]
                        # parsed_dict.append(self.parse_kv_rowbyrow(rows[i:], scores[i:,:]))
                        return self.recursive_parse(parsed_dict, rows[i:], scores[i:])
                        break
                    parsed_dict.append({h1: rows[i][0], h2: rows[i][1]})
            else:
                return self.parse_kv_rowbyrow(rows, scores)
                # TODO
        elif not merge_cell and width == 4:
            colon_inside = u'：' in (' '.join([x[:-1] if u'（' not in x else x.split(u'（')[0] for x in rows[0]]))
            if colon_inside:
                return self.parse_kv_rowbyrow(rows, scores)
            else:
                score1 = scores[0][1:].mean()
                score2 = scores[1][1:].mean()
                # if ratio2 > ratio1 * 2:
                if scores[:, ::2].mean() > 0.6 and scores[:, 1::2].mean() < 0.4:
                    parall = False
                    for i in xrange(len(rows)):
                        line = rows[i]
                        if line[0] == line[2] and scores[i][0] > 0.35:
                            parall = True
                    if parall:
                        h1 = rows[0][0].replace(u'：', '')
                        h2 = rows[0][2].replace(u'：', '')
                        d1 = {}
                        d2 = {}
                        for line in rows:
                            d1[line[0].replace(u'：', '')] = line[1]
                            d2[line[2].replace(u'：', '')] = line[3]
                        if u'☒' in d1:
                            del d1[u'☒']
                        if u'☒' in d2:
                            del d2[u'☒']
                        parsed_dict = [d1, d2]
                    else:
                        parsed_dict = {}
                        for line in rows:
                            parsed_dict[line[0].replace(u'：', '')] = line[1]
                            parsed_dict[line[2].replace(u'：', '')] = line[3]
                        if u'☒' in parsed_dict:
                            del parsed_dict[u'☒']
                            # TODO
                else:  # elif ratio1 > ratio2 * 2 and u'：' not in rows[0][0][:-1]:
                    if score1 > 0.6 and score1 > 1.6 * score2 and len(set(rows[0])) == len(rows[0]):
                        parsed_dict = []
                        for i in xrange(1, len(rows)):
                            tmp_dict = {}
                            for j in xrange(width):
                                tmp_dict[rows[0][j].replace(u'：', '')] = rows[i][j]
                            parsed_dict.append(tmp_dict)
                        parsed_dict = [parsed_dict, ]
                    else:
                        return self.parse_kv_rowbyrow(rows, scores)
        elif width >= 3 and len(set(rows[0])) == width and scores[0].mean() > 0.6 and (
            (scores[1:, 1::2].mean() < 0.4 and scores[1:, 2::2].mean() < 0.4) or (
                rows[0][0] == u'序号' and rows[1][0].isdigit())):
            parsed_dict = []
            for i in xrange(1, len(rows)):
                tmp_dict = {}
                for j in xrange(width):
                    tmp_dict[rows[0][j].replace(u'：', '')] = rows[i][j]
                parsed_dict.append(tmp_dict)
            parsed_dict = [parsed_dict, ]
        else:
            # print u'\t'.join(rows[0])
            return self.parse_kv_rowbyrow(rows, scores)
        return parsed_dict

    def parse_kv_rowbyrow(self, rows, scores):
        parsed_dict = {}

        if len(rows) == 0:
            return []

        if len(rows) > 2 and len(rows[0]) > 2 and len(rows[0]) == len(rows[1]) and len(rows[1]) == len(
                rows[2]) and np.mean(np.array(scores[:3])[1:3, 0]) > 0.65 and (
                np.max(np.mean(np.array(scores[:3])[:3, 1:], axis=0)) < 0.35 or (
                np.max(np.mean(np.array(scores[:3])[1:, 1:], axis=0)) < 0.35 and len(
                set.intersection(*[set(x.replace(u'：', '').strip()) for x in rows[0][1:]])) > 0)):
            anchor = len(rows)
            parsed_dict = []

            for i in xrange(3, len(rows)):
                if len(rows[i]) != len(rows[0]) or (scores[i][0] < 0.5 or np.mean(scores[i][1:]) > 0.6) or rows[i + 1][
                    0] == u'→':
                    anchor = i
                    break

            for i in xrange(1, len(rows[0])):
                dd = {}
                if u'候选' in rows[0][i]:
                    dd[rows[0][i]] = rows[1][i]
                for j in xrange(anchor):
                    dd[rows[j][0]] = rows[j][i]
                parsed_dict.append(dd)
            parsed_dict = [parsed_dict, ]

            if anchor > len(rows) - 1:
                return parsed_dict
            else:
                return self.recursive_parse(parsed_dict, rows[anchor:], scores[anchor:])

        elif len(rows) >= 2 and rows[1][0] == u'→' and len(rows[1]) > 1 and rows[1][1] != u'→' and rows[0][
            0] != u'→' and (np.mean(scores[1][1:]) > 0.15 or u'：' in (rows[0][1][:-1] + rows[1][1][:-1])):
            key = rows[0][0].replace(u'：', '')
            line = rows[0][1:]
            ss = scores[0][1:]

            if len(line) == 1 and scores[0][0] > 0.5 and scores[0][1] < 0.4 and rows[0][1].count(
                    u'：') == 1 and self.key_checker.score(rows[0][1].split(u'：')[0]) > 0.5:
                parsed_dict = [[rows[0][0]], {rows[0][1].split(u'：')[0]: rows[0][1].split(u'：')[1]}]
            elif len(line) == 1 and scores[0][0] > 0.5 and scores[0][1] < 0.4:
                parsed_dict = [[rows[0][0]], {rows[0][0]: rows[0][1]}]
            elif len(line) % 2 == 0 and np.mean(ss[::2]) > 0.6 and np.mean(ss[1::2]) < 0.5:
                parsed_dict = [key, ]
                dd = {}
                for j in xrange(0, len(line), 2):
                    dd[key + line[j]] = line[j + 1]
                parsed_dict.append(dd)
            elif len(line) % 2 == 1 and len(line) > 2 and np.mean(ss[1::2]) > 0.6 and np.mean(ss[2::2]) < 0.5:
                parsed_dict = [key, ]
                dd = {}
                dd[key] = line[0]
                for j in xrange(1, len(line), 2):
                    dd[line[j]] = line[j + 1]  #
                parsed_dict.append(dd)
            elif u'：' in (rows[0][1][:-1] + rows[1][1][:-1]) and (rows[0][1] + rows[1][1]).count(u'：') >= 2:
                parsed_dict = [key, ]
                dd = {}
                for x in rows[0][1:]:
                    if u'：' in x and self.key_checker.score(x.split(u'：')[0]) > 0.5:
                        dd[x.split(u'：')[0]] = u'：'.join(x.split(u'：')[1:]).strip()
                parsed_dict.append(dd)
            else:
                parsed_dict = [rows[0]]

            i = 1
            for i in xrange(1, len(rows)):
                if rows[i][0] == u'→':
                    key = rows[0][0].replace(u'：', '')
                    tmp = rows[i][1].replace('(', u'（').replace(':', u'（').replace(u'：', u'（').replace(u'名称', u'（')
                    tmp = tmp.split(u'（')[0]
                    if any([tmp.endswith(x) for x in self.turning_points]):
                        parsed_dict.append({})
                    line = rows[i][1:]

                    if len(line) >= 1 and len(line) % 2 == 0 and np.mean(scores[i][1:][::2]) > 0.6 and np.mean(
                            scores[i][1:][1::2]) < 0.5 and u'：' not in rows[i][1].strip()[:-1]:
                        for j in xrange(0, len(line), 2):
                            if isinstance(parsed_dict[-1], dict):
                                parsed_dict[-1][key + line[j]] = line[j + 1]
                            else:
                                parsed_dict.append({})
                                parsed_dict[-1][key + line[j]] = line[j + 1]
                    elif len(line) >= 1 and len(line) % 2 == 1 and np.mean(scores[i][1:][1::2]) > 0.6 and np.mean(
                            scores[i][1:][::2]) < 0.5 and u'：' not in rows[i][1].strip()[:-1]:
                        parsed_dict.append({key: line[0]})
                        for j in xrange(1, len(line), 2):
                            if isinstance(parsed_dict[-1], dict):
                                parsed_dict[-1][line[j]] = line[j + 1]
                            else:
                                parsed_dict.append({})
                                parsed_dict[-1][line[j]] = line[j + 1]
                    elif u'：' in ''.join([x[:-1] for x in rows[i][1:]]) and (''.join([x for x in rows[i][1:]])).count(
                            u'：') >= len(rows[i]) - 1:
                        for x in rows[i][1:]:
                            if x.count(u'：') == 1 and self.key_checker.score(x.split(u'：')[0]) > 0.5:
                                if isinstance(parsed_dict[-1], dict):
                                    parsed_dict[-1][x.split(u'：')[0]] = u'：'.join(x.split(u'：')[1:]).strip()
                                else:
                                    parsed_dict.append({})
                                    parsed_dict[-1][x.split(u'：')[0]] = u'：'.join(x.split(u'：')[1:]).strip()
                            else:
                                parsed_dict.append([x])
                    else:
                        parsed_dict.append(rows[i][1:])
                        # return [parsed_dict, ]
                        return self.recursive_parse([parsed_dict, ], rows[i:], scores[i:])
                else:
                    return self.recursive_parse([parsed_dict, ], rows[i:], scores[i:])
            parsed_dict = [parsed_dict, ]
            # return self.recursive_parse([parsed_dict,], rows[i:], scores[i:])

        elif len(rows[0]) == 4 and np.mean(scores[0][::2]) >= 0.6 and np.mean(scores[0][1::2]) < 0.45:
            row_4 = [0, ]
            row_l4 = []
            row_n4 = []
            parall = 0
            anchor = len(rows)
            i = -1
            for i in xrange(1, len(rows)):
                tmp = rows[i][0].replace('(', u'（').replace(':', u'（').replace(u'：', u'（').replace(u'名称', u'（')
                tmp = tmp.split(u'（')[0]
                if i < len(rows) - 1 and rows[i + 1][0] == u'→':
                    anchor = i
                    break
                if any([tmp.endswith(x) for x in self.turning_points]):
                    anchor = i
                    break
                if len(rows[i]) == 1 or (len(rows[i]) > 2 and np.mean(scores[i]) > 0.65) or len(
                        [x for x in rows[i] if x != u'☒']) > 4:  # or (len(rows[i])<=1 and i != len(rows)-1)
                    anchor = i
                    break

                if len(rows[i]) == 4 and np.mean(scores[i][::2]) > 0.6 and np.mean(scores[i][1::2]) < 0.5:
                    if rows[i][0].replace(u'：', '') == rows[i][2].replace(u'：', ''):
                        parall += 1
                    row_4.append(i)
                elif len([x for x in rows[i] if x != u'☒']) <= 4 and np.mean(
                        [scores[i][j] for j, x in enumerate(rows[i]) if x != u'☒']) > 0.25:  # and rows[i][0] != u'☒':
                    ll = [x.replace(u'：', '') for x in rows[i] if x != u'☒']
                    if len(ll) == 3 and (ll[0] == ll[1] or ll[0] == ll[2]):
                        parall += 1
                    elif len(ll) == 2 and ll[0] == ll[1]:
                        parall += 1
                    row_l4.append(i)
                else:
                    anchor = i
                    break
            # print rows[0][0], anchor, len(row_4), len(row_l4), len(row_n4), parall
            # print 'anchor', anchor
            if parall >= 2:
                parsed_dict = []
                d1 = {}
                d2 = {}
                for i in xrange(anchor):
                    if i in row_4:
                        d1[rows[i][0].replace(u'：', '')] = rows[i][1]
                        d2[rows[i][2].replace(u'：', '')] = rows[i][3]
                    elif i in row_l4:
                        rows[i] = [x for x in rows[i] if x != u'☒']
                        if len(rows[i]) == 2 and rows[i][0] == rows[i][1]:
                            continue
                        elif len(rows[i]) == 3 and rows[i][0].replace(u'：', '') == rows[i][1].replace(u'：', ''):
                            d1[rows[i][0].replace(u'：', '')] = ''
                            d2[rows[i][1].replace(u'：', '')] = rows[i][2]
                        elif len(rows[i]) == 3 and rows[i][0].replace(u'：', '') == rows[i][2].replace(u'：', ''):
                            d1[rows[i][0].replace(u'：', '')] = rows[i][1]
                            d2[rows[i][2].replace(u'：', '')] = ''
                        elif len(rows[i]) == 4 and rows[i][0].replace(u'：', '') == rows[i][2].replace(u'：', ''):
                            d1[rows[i][0].replace(u'：', '')] = rows[i][1]
                            d2[rows[i][2].replace(u'：', '')] = rows[i][3]
                        elif len(rows[i]) == 2 and self.key_checker.score(rows[i][0]) > 0.5 and self.key_checker.score(
                                rows[i][1]) < 0.5:
                            parsed_dict.append({rows[i][0].replace(u'：', ''): rows[i][1]})
                        # else:
                        elif len(rows[i]) == 3 and self.key_checker.score(rows[i][1]) > 0.6 and self.key_checker.score(
                                rows[i][2]) < 0.4:
                            parsed_dict.append([rows[i][0], {rows[i][1].replace(u'：', ''): rows[i][2]}])
                        elif len(rows[i]) == 1 and rows[i][0].count(u'：') == 1 and self.key_checker.score(
                                rows[i][0].split(u'：')[0]) > 0.6:
                            parsed_dict.append({rows[i][0].split(u'：')[0]: rows[i][0].split(u'：')[1]})
                        else:
                            parsed_dict.append(rows[i])
                parsed_dict = [d1, d2] + parsed_dict
            else:
                parsed_dict = {}
                for i in xrange(anchor):
                    if i in row_4 and np.mean(scores[i][::2]) > 0.6 and np.mean(scores[i][1::2]) < 0.5:
                        parsed_dict[rows[i][0].replace(u'：', '')] = rows[i][1]
                        parsed_dict[rows[i][2].replace(u'：', '')] = rows[i][3]
                    elif i in row_l4 and len(rows[i]) == 2 and scores[i][0] >= 0.6 and scores[i][1] <= 0.4:
                        parsed_dict[rows[i][0].replace(u'：', '')] = rows[i][1]
                    elif i in row_l4 and len(rows[i]) == 4 and rows[i][0] == u'☒' and rows[i][1] == u'☒' and scores[i][
                        2] > 0.6 and scores[i][3] < 0.4:
                        parsed_dict[rows[i][2].replace(u'：', '')] = rows[i][3]
                    elif i in row_l4 and len(rows[i]) == 4 and rows[i][2] == u'☒' and rows[i][3] == u'☒' and scores[i][
                        0] > 0.6 and scores[i][1] < 0.4:
                        parsed_dict[rows[i][0].replace(u'：', '')] = rows[i][1]
                parsed_dict = [parsed_dict, ]
            if anchor > len(rows) - 1:
                return parsed_dict
            else:
                # return self.recursive_parse([parsed_dict,], rows[anchor:], scores[anchor:])
                return self.recursive_parse(parsed_dict, rows[anchor:], scores[anchor:])

        elif len(rows[0]) == 2 and u'：' in rows[0][0] and u'：' in rows[0][1] and self.key_checker.score(
                rows[0][0].split(u'：')[0]) > 0.5 and self.key_checker.score(rows[0][1].split(u'：')[0]) > 0.5:
            row_2 = [0, ]
            row_l2 = []
            parall = 0
            anchor = len(rows)
            i = -1
            for i in xrange(1, len(rows)):
                row = rows[i]
                row = [x for x in row if x != u'☒']
                if len(row) == 2:
                    if i < len(rows) - 1 and rows[i + 1][0] == u'→':
                        anchor = i
                        break
                    if u'：' in row[0] and u'：' in row[1]:
                        ls = ''.join(row[0].split(u'：')[0].split())
                        rs = ''.join(row[1].split(u'：')[0].split())
                        if ls == rs:
                            parall += 1
                        row_2.append(i)
                    else:
                        # row_l2.append(i)
                        anchor = i
                        break
                elif len(row) == 1 and u'：' in row[0]:
                    row_l2.append(i)
                else:
                    anchor = i
                    break

            if parall >= 2:
                parsed_dict = []
                d1 = {}
                d2 = {}
                for i in xrange(anchor):
                    if i in row_2:
                        rows[i] = [x for x in rows[i] if x != u'☒']
                        d1[rows[i][0].split(u'：')[0].strip()] = u'：'.join(rows[i][0].split(u'：')[1:])
                        d2[rows[i][1].split(u'：')[0].strip()] = u'：'.join(rows[i][1].split(u'：')[1:])
                    # elif i in row_l2:
                    else:
                        parsed_dict.append(rows[i])
                if len(parsed_dict) != 0:
                    parsed_dict = [d1, d2, parsed_dict]
                else:
                    parsed_dict = [d1, d2]
            else:
                parsed_dict = []
                dd = {}
                for i in xrange(anchor):
                    tmp = \
                    rows[i][0].replace('(', u'（').replace(':', u'（').replace(u'：', u'（').replace(u'名称', u'（').split(
                        u'（')[0]
                    if any([tmp.endswith(x) for x in self.turning_points]):
                        if len(dd) > 0:
                            parsed_dict.append(dd)
                            dd = {}
                    if i in row_2:
                        rows[i] = [x for x in rows[i] if x != u'☒']
                        dd[rows[i][0].split(u'：')[0].strip()] = u'：'.join(rows[i][0].split(u'：')[1:])
                        dd[rows[i][1].split(u'：')[0].strip()] = u'：'.join(rows[i][1].split(u'：')[1:])
                    elif i in row_l2:  # and u'：' in rows[i][0]:
                        rows[i] = [x for x in rows[i] if x != u'☒']
                        dd[rows[i][0].split(u'：')[0].strip()] = u'：'.join(rows[i][0].split(u'：')[1:])
                    else:
                        parsed_dict.append(rows[i])
                if len(dd) > 0:
                    parsed_dict.append(dd)
            # print parsed_dict
            if anchor > len(rows) - 1:
                return parsed_dict
            else:
                # return self.recursive_parse([parsed_dict,], rows[anchor:], scores[anchor:])
                return self.recursive_parse(parsed_dict, rows[anchor:], scores[anchor:])

        elif rows[0][0] != u'→' and len(rows[0]) > 2 and u'：' in ''.join(rows[0]) and check_colon_table(rows[0]):
            parsed_dict = []
            for i in xrange(len(rows)):
                if i == 0 or check_colon_table(rows[i]):
                    parsed_dict_ = []
                    for x in rows[i]:
                        if u'：' in x:
                            parsed_dict_.append({x.split(u'：')[0]: u'：'.join(x.split(u'：')[1:])})
                        elif ':' in x:
                            parsed_dict_.append({x.split(u'：')[0]: u'：'.join(x.split(u'：')[1:])})
                        else:
                            parsed_dict_.append(x)
                    parsed_dict.append(parsed_dict_)
                else:
                    return self.recursive_parse(parsed_dict, rows[i:], scores[i:])
                    break


        elif ((len(rows) > 1 and rows[1][0] != u'→') or (len(rows) == 1)) and len(rows[0]) >= 2 and np.mean(
                scores[0][::2]) > 0.65 and np.mean(
                scores[0][1::2]) < 0.4:  # and scores[0][0] > 0.6  # and len(rows[i])%2 == 0
            anchor = len(rows)
            i = 0
            while (i < len(rows)):
                tmp = rows[i][0].replace('(', u'（').replace(':', u'（').replace(u'：', u'（').replace(u'名称', u'（')
                tmp = tmp.split(u'（')[0]
                if i < len(rows) - 1 and rows[i + 1][0] == u'→':
                    anchor = i
                    break
                if any([tmp.endswith(x) for x in self.turning_points]) and i != 0:
                    anchor = i
                    break
                if (((i < len(rows) - 1 and rows[i + 1][0] != u'→') or (i == len(rows) - 1)) and np.mean(
                        scores[i][::2]) > 0.65 and np.mean(scores[i][1::2]) < 0.5):
                    for j in xrange(0, len(rows[i]), 2):
                        if scores[i][j] > 0.5 and j < len(rows[i]) - 1:
                            parsed_dict[rows[i][j]] = rows[i][j + 1]
                        elif scores[i][j] > 0.5 and j == len(rows[i]) - 1:
                            parsed_dict[rows[i][j]] = ''
                elif len(rows[i]) == 4 and rows[i][0] == u'☒' and rows[i][1] == u'☒' and scores[i][2] > 0.65 and \
                                scores[i][3] < 0.4:
                    parsed_dict[rows[i][2].replace(u'：', '')] = rows[i][3]
                elif len(rows[i]) == 4 and rows[i][2] == u'☒' and rows[i][3] == u'☒' and scores[i][0] > 0.65 and \
                                scores[i][1] < 0.4:
                    parsed_dict[rows[i][0].replace(u'：', '')] = rows[i][1]
                else:
                    anchor = i
                    break
                i += 1

            if i > len(rows) - 1:
                return parsed_dict
            else:
                return self.recursive_parse([parsed_dict, ], rows[anchor:], scores[anchor:])

        # elif len(rows[0]) > 2 and len(rows[0])%2==0 and np.mean(scores[0][::2])>0.65 and np.mean(scores[0][1::2])<0.4:
        #    parsed_dict = {}
        #    for j in xrange(0, len(rows[0]), 2):
        #        parsed_dict[rows[0][j].replace(u'：','')] = rows[0][j+1]
        #    return self.recursive_parse([parsed_dict,], rows[anchor:], scores[anchor:])

        elif len(rows) >= 2 and len(rows[0]) == len(rows[1]) and np.mean(scores[0][1:]) > 0.75 and np.mean(
                scores[1][1:]) < 0.4 and len(set(rows[0])) == len(rows[0]):
            # print '$'.join(rows[0])
            anchor = len(rows)
            parsed_dict = []
            i = -1
            for i in xrange(1, len(rows)):
                # if i < len(rows)-1 and rows[i+1][0]==u'→':
                #    anchor = i
                #    break
                if (len(rows[i]) != len(rows[0]) or np.mean(scores[i][1:]) >= 0.5):
                    anchor = i
                    break
                dd = {}
                for j in xrange(len(rows[0])):
                    dd[rows[0][j].replace(u'：', '')] = rows[i][j]
                parsed_dict.append(dd)

            if anchor > len(rows) - 1:
                return [parsed_dict, ]
            else:
                return self.recursive_parse([parsed_dict, ], rows[anchor:], scores[anchor:])
        elif (len(rows[0]) > 4 or len(rows[0]) == 3) and ''.join(rows[0]).count(u'：') >= len(rows[0]) and ''.join(
                [x[:-1] for x in rows[0]]).count(u'：') >= len(rows[0]) - 3 and np.mean(
                self.key_scores([[x.split(u'：')[0] for x in rows[0]]])[1]):
            dd = {}
            for j in xrange(len(rows[0])):
                dd[rows[0][j].split(u'：')[0].strip()] = u'：'.join(rows[0][j].split(u'：')[1:])
            return self.recursive_parse([dd, ], rows[1:], scores[1:])

        elif len(rows) >= 2 and len(rows[0]) == 3:
            if scores[0][0] > 0.6 and scores[0][1] > 0.6 and scores[0][2] < 0.4:
                parsed_dict = {rows[0][0].replace(u'：', ''): '', rows[0][1].replace(u'：', ''): rows[0][2]}
            elif scores[0][0] > 0.6 and scores[0][1] < 0.4 and scores[0][2] > 0.6:
                parsed_dict = {rows[0][0].replace(u'：', ''): '', rows[0][1].replace(u'：', ''): rows[0][2]}
            elif scores[0][0] < 0.5 and u'：' in rows[0][1][:-1] and u'：' in rows[0][2][:-1]:
                parsed_dict = {rows[0][1].split(u'：')[0].strip(): rows[0][1].split(u'：')[1].strip(),
                               rows[0][2].split(u'：')[0].strip(): rows[0][2].split(u'：')[1].strip()}
            else:
                parsed_dict = rows[0]
            return self.recursive_parse([parsed_dict, ], rows[1:], scores[1:])
        else:
            return self.recursive_parse([rows[0], ], rows[1:], scores[1:])
        return parsed_dict

    def parse_kv(self, rows, scores=None):
        if len(rows) == 0:
            return []

        if scores is None:
            _, scores = self.key_scores(rows)

        colnums = [len(x) for x in rows]
        parsed_dict = []

        if colnums.count(colnums[0]) == len(colnums) and colnums[0] != 1:
            parsed_dict = self.parse_kv_matrix(rows, scores, colnums[0])
        elif len(rows[0]) == 1:
            isolated = [self.v2kv(rows[0][0]), ]
            anchor = len(rows)
            i = 0
            for i in xrange(1, len(rows)):
                row = rows[i]
                if len(row) == 1:
                    res = self.v2kv(row[0])
                    if isinstance(res, dict) and isinstance(isolated[-1], dict) and res.keys()[0] not in isolated[
                        -1] and not any([res.keys()[0].endswith(x) for x in self.turning_points]):
                        isolated[-1][res.keys()[0]] = res[res.keys()[0]]
                    # elif isinstance(res, list):
                    #    pass#isolated.append(res[0])
                    else:
                        isolated.append(res)
                else:
                    anchor = i
                    break
            if i == len(rows) - 1 and anchor != len(rows) - 1:
                anchor = len(rows)
            if len(isolated) == 1 and isinstance(isolated[0], dict):
                isolated = isolated[0]
            # if len(isolated) == 1 and isinstance(isolated[0], list):
            #    isolated = isolated[0]

            if anchor < len(rows):
                if len(set(colnums[anchor:])) == 1:
                    parsed_dict = self.parse_kv_matrix(rows[anchor:], scores[anchor:], colnums[anchor])
                else:
                    parsed_dict = self.parse_kv_rowbyrow(rows[anchor:], scores[anchor:])

                if not isinstance(isolated, list):
                    isolated = [isolated, ]
                if not isinstance(parsed_dict, list):
                    parsed_dict = [parsed_dict, ]

                '''if isinstance(parsed_dict[0], dict) and isinstance(isolated[-1], dict) and len(set(parsed_dict[0].keys()).intersection(isolated[-1].keys()))==0:
                    a = parsed_dict[0]
                    b = isolated[-1]
                    a.update(b)
                    parsed_dict =  isolated[:-1] + [a,] + parsed_dict[1:]
                else:
                    parsed_dict = isolated + parsed_dict'''
                parsed_dict = isolated + parsed_dict
            else:
                parsed_dict = isolated
        else:
            parsed_dict = self.parse_kv_rowbyrow(rows, scores)
        return parsed_dict

    def exclude_tags(self, text):
        rec1 = re.compile('</.*?>')
        results1 = re.findall(rec1, text)

        rec2 = re.compile('<[^>]*?/>')
        results2 = re.findall(rec2, text)
        results2 = [x.split()[0] + '[^>]*?/>' for x in results2 if
                    ' ' in x and len(x.split()[0]) > 1 and x[:3] != '<td' and x[:3] != '<th']
        results2 = list(set(results2))

        results = list(set(
            results1 + ['</tbody>'] + ['</span>'] + ['</p>'] + ['</input>'] + ['</img>'] + ['</col>'] + ['</font>']))
        table_seps = ['</table>', '</tr>', '</td>', '</th>']
        for x in table_seps:
            if x in results:
                results.remove(x)
        results = [x.lower() for x in results] + [x.upper() for x in results]
        excluted_tags = [x[:2] + '*' + x[2:-1] + '[^>]*?' + x[-1] for x in results] + results2
        excluted_tags = '<!--[^>]*?-->|' + '|'.join(
            excluted_tags) + '|<a href[^>]*?>' + '|&#\d*;' + '|&[A-Za-z0-9]+;' + '|<![^>]*?>' + '|#[^>]*?{[^>]*?}' + '|<\?xml[^>]*?>'
        # + '|/\*[^>]*?\*/' + '|function[^>]*?{[^>]*?}'   #'|<script[^>]*?>[^>]*?</script>' +  + '|\.gundon[^>]*?{[^>]*?}' + '|</col.*?>' +'|<col.*?>' + 
        return excluted_tags

    def tags_cleaning(self, raw_html, excluded):
        # print excluded
        cleanr = re.compile(excluded)
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = re.sub('<table[^>]*?>', '<table>', cleantext)
        return cleantext

    def html_cleaning(self, doc):
        # print doc
        if isinstance(doc, str):
            try:
                doc = doc.decode('utf-8', 'ignore')
            except:
                try:
                    doc = doc.decode('gbk', 'ignore')
                except:
                    pass
        '''soup = bs(doc)
        for item in soup.findAll('script'):
            item.clear()
        doc = str(soup)'''

        doc = doc.replace('\t', '').replace('<TABLE', '<table').replace('</TABLE', '</table').replace('<TR',
                                                                                                      '<tr').replace(
            '</TR', '</tr')
        doc = doc.replace('<TD', '<td').replace('</TD', '</td').replace('<TH', '<th').replace('</TH', '</th').replace(
            '<TBODY>', '').replace('</TBODY>', '').replace('<tbody>', '').replace('</tbody>', '')
        doc = doc.replace('&nbsp;', '').replace('nbsp;', '').replace('<BR />', '\n').replace('<BR/>', '\n').replace(
            '<BR>', '\n').replace('<br />', '\n').replace('<br/>', '\n').replace('<br>', '\n')
        doc = doc.replace('&sup', '^').replace('&yen', '¥').replace('&ldquo;', u'“').replace('&rdquo;', u'”').replace(
            '&gt;', u'≻').replace('&lt;', u'≺')
        doc = re.sub('&', '', doc)

        excluted_tags = self.exclude_tags(doc)
        doc = self.tags_cleaning(doc, excluted_tags)
        doc = doc.replace('begin-->', '').replace('end-->', '')
        return doc

    def parse(self, doc):
        doc = self.html_cleaning(doc)
        # print doc
        soup = bs(doc)

        tables = soup.findAll("table")
        # print len(tables)

        descs = []
        tbs = []
        table_count = 0
        for table in tables:
            table_count += 1
            desc = table.previousSibling
            # print desc
            if desc is None:
                desc = ''
            else:
                desc = str(desc).strip()
                if desc != '':
                    desc = desc.split()[-1]  # [-50:]
            try:
                desc = desc.decode('utf-8')
            except:
                pass

            if u'业绩' in desc[-20:] and table_count > 1:
                continue

            table2 = str(table)
            table2 = table2.decode('utf-8')
            # print table2

            try:
                table = etree.XML(table2)
            except:
                try:
                    table2 = self.cleaner.clean_html(table2)
                    table = etree.XML(table2)
                except:
                    # table = etree.XML(table2)
                    # print table2
                    # print 'fail'
                    continue

            lst = []
            lst2 = []
            rowspans_list = []
            colspans_list = []
            rows = iter(table)

            longest_string = ''
            longest_string_len = 0
            for row in rows:
                try:
                    values = [col.text.decode('utf-8').strip() if col.text is not None else u'☒' for col in
                              row]  # ㍿  ☆ ☒ →
                except:
                    values = [col.text.strip() if col.text is not None else u'☒' for col in row]

                for val in values:
                    if len(val) > longest_string_len:
                        longest_string = val
                        longest_string_len = len(val)

                values = [_.replace(u':', u'：') for _ in values]
                vs = []
                ct = 0
                rowspans = []
                colspans = []
                # print '\t'.join(values)
                while ct < len(values):
                    if 'rowspan' in row[ct].attrib:
                        try:
                            rowspan = int(re.findall('[\d]+', row[ct].attrib['rowspan'])[0])
                            rowspans.append(rowspan)
                        except:
                            rowspans.append(1)
                    else:
                        rowspans.append(1)

                    if 'colspan' in row[ct].attrib:
                        try:
                            colspan = int(re.findall('[\d]+', row[ct].attrib['colspan'])[0])
                            colspans.append(colspan)
                        except:
                            rowspans.append(1)
                    else:
                        colspans.append(1)

                    item = ' '.join(values[ct].strip().split())
                    if item == '':
                        item = u'☒'
                    if ct < len(values) - 1:
                        if values[ct + 1] == u'：':
                            item = item + u'：'
                            ct += 1
                    # if len(''.join(item.split())) < 30 and not (''.join(item.split())).isdigit() and self.key_checker.score(''.join(item.split())) >= 0.5:
                    #    item = ''.join(item.split())
                    elif u'：' in item:
                        ls = item.split(u'：')[0]
                        rs = u'：'.join(item.split(u'：')[1:])
                        item = ''.join(ls.split()) + u'：' + rs
                    ct += 1
                    vs.append(item.replace('\n', u'  '))

                # if len(set(vs)) == 0:
                #    continue

                lst.append(vs)
                rowspans_list.append(rowspans)
                colspans_list.append(colspans)

                # print ' $ '.join(vs)
            # print longest_string, doc.count(longest_string), u'业绩' in doc.split(longest_string)[0]
            if longest_string_len > 4 and doc.count(longest_string) == 1 and u'业绩' in doc.split(longest_string)[0]:
                continue

            for i, line in enumerate(lst):
                rowspans = rowspans_list[i]
                colspans = colspans_list[i]
                indents = 0
                if len(line) == 0:
                    continue
                if i == 0 and (line[0] == u'☒' or line[0] == u'') and rowspans.count(1) == len(rowspans):
                    continue
                if (line.count(u'☒') + line.count(u'→') + line.count(u'')) == len(line):
                    continue

                if len(rowspans) > 1 and (rowspans[0] > 1 or line[0] == u'→'):
                    not0 = []
                    s_1 = []
                    s_2 = []
                    for j, r in enumerate(rowspans):
                        if lst[i][0] != u'→' and r != 1 and (
                                j == 0 or (len(s_1) > 0 and j == max(s_1) + 1 and r <= rowspans[s_1[-1]])):
                            s_1.append(j)
                        elif lst[i][0] == u'→' and lst[i][j] != u'→' and r != 1 and (
                                len(s_2) == 0 or (len(s_2) > 0 and j == max(s_2) + 1)):
                            s_2.append(j)

                        # if r == rowspans[0] and len(not0)==0:
                        #    indents += 1
                        # if r != rowspans[0]:
                        if r == 1:
                            not0.append(j)

                    if len(s_1) > 0:
                        indents = s_1[-1] + 1
                        for j in s_1:
                            for ct in xrange(i + 1, min(i + rowspans[j], len(lst))):
                                lst[ct].insert(j, u'→')
                                rowspans_list[ct].insert(j, 1)
                                colspans_list[ct].insert(j, colspans_list[i][j])
                    elif len(s_2) > 0:
                        indents = s_2[-1] + 1
                        for j in s_2:
                            for ct in xrange(i + 1, min(i + rowspans[j], len(lst))):
                                lst[ct].insert(j, u'→')
                                rowspans_list[ct].insert(j, 1)
                                colspans_list[ct].insert(j, colspans_list[i][j])
                                # lst[ct] = [u'→'] + lst[ct]
                                # rdowspans_list[ct] = [1] + rowspans_list[ct]
                                # colspans_list[ct] = [colspans_list[i][j]] + colspans_list[ct]
                    else:
                        indents = 1

                    if lst[i][0] != u'→' and i + 2 < len(lst) and len(not0) > 0 and len(not0) < len(
                            rowspans_list[i]) and (rowspans_list[i].count(1) + rowspans_list[i].count(2)) == len(
                            rowspans_list[i]) and sum(colspans_list[i]) == sum(colspans_list[i + 2]):
                        not1 = [j for j, x in enumerate(lst[i + 1]) if x != u'→']
                        colsp0 = [colspans_list[i][j] for j in not0]
                        colsp1 = [colspans_list[i + 1][j] for j in not1]
                        lst1 = [lst[i + 1][j] for j in not1]
                        cumsum0 = list(accumulate(colsp0))
                        cumsum1 = list(accumulate(colsp1))
                        marks = [0, ]
                        for j in xrange(len(cumsum0)):
                            # if len(marks)==0:
                            for h in xrange(marks[-1], len(cumsum1)):
                                if cumsum0[j] == cumsum1[h]:
                                    marks.append(h + 1)
                                    break
                        ct = 0
                        if sum(colsp0) == sum(colsp1) and len(marks) == len(colsp0) + 1:
                            ks = []
                            colspans_ = []
                            for j in xrange(len(lst[i])):
                                if j not in not0:
                                    ks.append(lst[i][j])
                                    colspans_.append(colspans_list[i][j])
                                else:
                                    for h in xrange(marks[ct], marks[ct + 1]):
                                        ks.append(lst1[h])
                                        colspans_.append(colsp1[h])
                                    ct += 1

                            vs = lst[i + 2]
                            if len(ks) > 2 and (len(ks) == len(vs)) and np.mean(
                                    self.key_scores([ks])[1]) > 0.6 and np.mean(self.key_scores([vs])[1]) < 0.45:
                                # lst[i] = ['|'+'|'.join([lst[i][t] for t in not0])+'|', '|'+'|'.join([x for x in lst[i+1] if x != u'→'])+'|']
                                lst[i] = ['|' + lst[i][not0[j]] + '|' + u'≡' + '|' + '|'.join(
                                    [x for x in lst1[marks[j]:marks[j + 1]]]) + '|' for j in xrange(len(not0))]
                                lst[i + 1] = ks
                                rowspans_list[i] = [1] * len(lst[i])
                                rowspans_list[i + 1] = [1] * len(lst[i + 1])
                                colspans_list[i] = [1] * len(lst[i])
                                colspans_list[i + 1] = colspans_

                indents = max(1, indents)
                rowspans = rowspans_list[i]
                # colspans = colspans_list[i]

                for index, j in enumerate(rowspans[indents:]):
                    if j > 1 and len(lst) > i + 1 and len(lst[i + 1]) - 1 < len(lst[i]):  # doubtful
                        # for l in lst[i+1:i+j]:
                        for t in xrange(i + 1, min(i + j, len(lst))):
                            lst[t].insert(index + indents, lst[i][index + indents])
                            rowspans_list[t].insert(index + indents, 1)
                            colspans_list[t].insert(index + indents, colspans_list[i][index + indents])
                            # lst[t].insert(len(lst[t])-index, lst[i][-index-1])
                            # rowspans_list[t].insert(len(lst[t])-index, 1)

            for i, line in enumerate(lst):
                if i >= len(lst):
                    break
                colspans = colspans_list[i]
                if (lst[i].count(u'→') + lst[i].count(u'☒')) == len(lst[i]):
                    del lst[i]
                    del rowspans_list[i]
                    del colspans_list[i]
                elif lst[i].count(u'→') > 4 and lst[i].count(u'→') == len(lst[i - 1]) and len(lst[i]) == 2 * len(
                        lst[i - 1]):
                    width = len(lst[i - 1])
                    lst[i] = lst[i][width:]
                    colspans_list[i] = colspans_list[i][width:]
                    rowspans_list[i] = rowspans_list[i][width:]
                elif (i == 0 or (i > 0 and np.mean(self.key_scores([lst[i - 1]])[1]) < 0.67 and not (
                        lst[i - 1][0] == u'→' and len(lst[i]) == len(lst[i - 1])))) and len(lst[i]) > 2 and i + 2 < len(
                        lst) and len(lst[i + 1]) > 2 and lst[i][0] != u'→' and lst[i + 1][0:2] == [u'→', u'→'] and lst[
                                                                                                                               i + 1][
                                                                                                                   0:3] != [
                    u'→', u'→', u'→'] and lst[i + 1].count(u'→') != len(
                        lst[i + 1]):  # (lst[i+1].count('→')+lst[i+1].count('☒'))!=len(lst)
                    # print '\t'.join(lst[i])
                    # for j in xrange(i+1, len(lst)):
                    #    if
                    lst.insert(i, [lst[i][0]])
                    rowspans_list.insert(i, [rowspans_list[i][0]])
                    colspans_list.insert(i, [colspans_list[i][0]])
                    lst[i + 1] = lst[i + 1][1:]
                    rowspans_list[i + 1] = rowspans_list[i + 1][1:]
                    colspans_list[i + 1] = colspans_list[i + 1][1:]
                    for j in xrange(i + 2, len(lst)):
                        if lst[j][:1] == [u'→']:
                            lst[j] = lst[j][1:]
                            rowspans_list[j] = rowspans_list[j][1:]
                            colspans_list[j] = colspans_list[j][1:]
                        else:
                            break
                            # pass
                elif len(lst[i]) >= 2 and len(lst) > i + 1 and len(lst[i + 1]) > 0 and lst[i + 1][
                    0] != u'→' and colspans.count(1) < len(colspans) and len(colspans_list[i]) < len(
                        colspans_list[i + 1]) and sum(colspans_list[i]) == sum(colspans_list[i + 1]) and len(
                        set(list(accumulate(colspans_list[i]))).difference(set(list(accumulate(colspans_list[
                                                                                                           i + 1]))))) == 0:  # and colspans_list[i+1].count(1)==len(colspans_list[i+1]):
                    s0 = np.mean(self.key_scores([lst[i]])[1])
                    s1 = np.mean(self.key_scores([lst[i + 1][1:]])[1])
                    colspans_1 = colspans_list[i + 1]
                    cumsum0 = list(accumulate(colspans_list[i]))
                    cumsum1 = list(accumulate(colspans_list[i + 1]))
                    cum_ind = [cumsum1.index(_) for _ in cumsum0]
                    cum_ind = [-1] + cum_ind
                    cum_ind = [cum_ind[_] - cum_ind[_ - 1] for _ in range(1, len(cum_ind))]

                    if s0 > 0.65 and s1 < 0.35:
                        for t in xrange(i + 1, len(lst)):
                            if t > i + 1 and np.mean(self.key_scores([lst[t][1:]])[1]) > 0.35:
                                break
                            if colspans_list[t] == colspans_1:
                                count = 0
                                lt = []
                                ct = []
                                rt = []
                                for w, s in zip(colspans_list[i], cum_ind):
                                    lt.append(' | '.join(lst[t][count:count + s]))
                                    ct.append(w)
                                    rt.append(1)
                                    count += s
                                lst[t] = lt
                                colspans_list[t] = ct
                                rowspans_list[t] = rt

                # 针对http://www.8yu.cn/ZhaoBiao/2942340.html中的不规范表格的特殊处理
                if i < len(lst) - 1 and lst[i] == [u'包号', u'采购内容', u'中标供应商', u'成交金额'] and len(lst[i + 1]) == 3:
                    lst[i] = [u'包号 - 采购内容', u'中标供应商', u'成交金额']
                    colspans_list[i] = [colspans_list[i][0] + colspans_list[i][1]] + colspans_list[i][2:]
                    rowspans_list[i] = [rowspans_list[i][0] + rowspans_list[i][1]] + rowspans_list[i][2:]

            # for i, line in enumerate(lst):
            #    print '****', '\t'.join(line)

            lst1 = []
            lst2 = []

            for line in lst:
                # print line
                if len(set(line)) == 0 or (len(set(line)) == 1 and set(line) == set([u'☒'])) or (
                        len(set(line)) == 2 and set(line) == set([u'☒', u'→'])):
                    continue
                line_clean = filter(lambda a: a != u'→', line)
                if len(line_clean) == 0:  # or (len(line_clean)==1 and len(line_clean[0])>100):
                    continue
                lst1.append(line)
                # lst2.append([str(self.key_checker.score(item.replace(u'：','').replace('(',u'（').replace(')',u'）'))) for item in line])

            lst1 = self.drop_null_cols(lst1)

            if len(list(itertools.chain(*lst1))) < 1:
                continue

            col0 = self.get_col(lst1, 0)
            if col0[0] == u'☒' and col0.count(u'☒') > 5:
                for l in lst1:
                    if l[0] == u'☒':
                        l.pop(0)
                    else:
                        break

            lst2, lst3 = self.key_scores(lst1)
            try:
                parsed_dict = self.parse_kv(lst1, lst3)
            except:
                parsed_dict = []
            if isinstance(parsed_dict, list):
                parsed_dict = [x for x in parsed_dict if len(x) != 0]
                # if len(parsed_dict) == 1:
                #    parsed_dict = parsed_dict[0]
            if len(parsed_dict) == 0 or (
                        len(parsed_dict) == 1 and isinstance(parsed_dict, list) and type(parsed_dict[0]) not in [list,
                                                                                                                 dict]):  # in [str, unicode]
                continue
            '''
            types = [type(parsed_dict), ]
            for x in parsed_dict:
                #if type(x) == list:
                if isinstance(x, list):
                    types.append(list)
                    for item in x:
                        types.append(type(item))
                else:
                    types.append(type(x))
            if dict not in types:
                continue
            '''

            if DEBUG:
                jsoned = json.dumps(parsed_dict, ensure_ascii=False, encoding='utf-8')
                tbs.append(lst1 + lst2 + [[jsoned, ], ])
                descs.append(desc)
            else:
                tbs.append(parsed_dict)
                # return [tbs, descs]
        return tbs


def test():
    import urllib2

    # url = "http://www.zgazxxw.com/zbpd/zhongbgg/201610/2381101.php"
    # url = "http://www.xzztb.org/zbxx/1/?2015/9/1-3075.html"
    url = "http://www.sdzb.gov.cn/ZbGgGsShow.aspx?classid=5021&id=50781"
    # url = "http://www.jnggzy.gov.cn/art/2016/6/24/art_2103_254377.html"
    # url = "http://www.jnggzy.gov.cn/art/2016/8/30/art_2103_263917.html"
    # url = "http://www.hrbjjzx.cn/Bid_Front/TenderContent.aspx?ID=33204"
    # url = "http://www.hebgc.com/hebgc2009/?a=eng-anc-detail&xh=390131"

    url = "http://www.gsei.com.cn/html/1337/2016-11-28/content-148864.html"
    # url = "http://www.xzztb.org/zbxx/1/?2016-11-25-4651.html"
    url = "http://www.sczfcg.com/view/staticpags/zqyjgg/4028868754c88d0801550ff8cad14fc6.html"
    # url = "http://www.lntb.gov.cn/Article_Show.asp?ArticleID=768874"
    # url = "http://zb.cbi360.net/tb/20161129/10114775.html"
    # url = "http://www.lntb.gov.cn/Article_Show.asp?ArticleID=768879"
    # url = "http://www.hebgc.com/?a=eng-anc-detail&xh=397900"
    # url = "http://www.lntb.gov.cn/Article_Show.asp?ArticleID=478250"
    # url = "http://www.ccgp-hunan.gov.cn/portal/protalAction%21viewNoticeContent.action?noticeId=23136"
    # url = "http://www.ccgp-hunan.gov.cn/portal/protalAction%21viewNoticeContent.action?noticeId=1000033133"
    # url = "http://www.fjbid.gov.cn/zbgg1/zbgs/201612/t20161201_197280.htm"  #unbound prefix
    # url = "http://www.ahzfcg.gov.cn/news/2016-08/d6035827-1423-4cc5-b347-9a4104111f20.html"
    # url = "http://www.zjzfcg.gov.cn/detailPage?type=1&ID=9663880"
    # url = "http://www.zgazxxw.com/zbpd/zhongbgg/201610/2379408.php"
    # url = "http://www.zgazxxw.com/zbpd/zhongbgg/201610/2379708.php"
    # url = "http://www.gzzbw.cn/html/zbgg/gczb/20150716/162413.html"
    # url = "http://www.gzzbw.cn/html/zbgg/gczb/20150716/162405.html"
    # url = "http://www.gzzbw.cn/html/zbgg/gczb/20150709/161744.html"  #备注空
    # url = "http://www.gzzbw.cn/html/zbgg/gczb/20150723/163137.html"
    # url = "http://www.gzzbw.cn/html/zbgg/gczb/20141010/137214.html"
    # url = "http://www.xzztb.org/zbxx/1/?2015/9/1-3075.html"
    # url = "http://www.zgazxxw.com/zbpd/zhongbgg/201610/2380955.php"
    # url = 'http://www.zgazxxw.com/zbpd/zhongbgg/201610/2381079.php'
    # url = "http://www.tjconstruct.cn/shchxt/tonggao.doc/epr_zbgg/2016/ZBGG1404%5B2016%5D0705.htm"
    # url = "http://zb.cbi360.net/tb/20161102/9742833.html"
    # url = 'http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie/dllpekfeaoobbboejmmogmdlofcghili.do?isfloat=1&disp_template=pchlilmiaebdbboeljehjhkjkkgjbjie&fileid=50411048&moduleIDPage=dllpekfeaoobbboejmmogmdlofcghili&siteIDPage=gdcourt&infoChecked=null'
    # url = "http://www.sntba.com/website/news_show.aspx?id=34231"
    # url = "http://www.gsei.com.cn/html/1337/2016-11-28/content-148899.html"
    # url = "http://qhzbtb.qhwszwdt.gov.cn/qhweb/InfoDetail/Default.aspx?InfoID=8339a15d-cdef-4769-9abd-7bee052e8ed5&amp%3BCategoryNum=005001001"
    # url = "http://qhzbtb.qhwszwdt.gov.cn/qhweb/InfoDetail/Default.aspx?InfoID=d194547b-9654-4966-becc-49d8fed8c497&amp%3BCategoryNum=005001001"
    # url = 'http://www.jnggzy.gov.cn/art/2016/7/4/art_2103_255663.html'
    url = 'http://www.jxtb.org.cn/jxzbtb/zbgg/20161117/122257.htm'
    url = 'http://www.jnggzy.gov.cn/art/2016/4/19/art_2102_37861.html'
    url = 'http://www.bjztb.gov.cn/zbgg_2015/201611/t10636817.htm'
    url = 'http://www.ccgp-hunan.gov.cn/portal/protalAction!viewNoticeContent.action?noticeId=27576'
    url = 'http://www.ccgp-jiangsu.gov.cn/pub/jszfcg/cgxx/cggg/201611/t20161121_107223.html'
    url = 'http://www.ynbidding.net/content.aspx?id=938266484568'
    url = 'http://www.zgazxxw.com/zbpd/zhongbgg/201609/2300040.php'
    url = 'http://www.zgazxxw.com/zbpd/zhongbgg/201609/2300242.php'
    url = 'http://www.zgazxxw.com/zbpd/zbgg/201610/2366369.php'
    url = 'http://www.ynbidding.net/content.aspx?id=938266484568'
    url = 'http://www.ccgp-jiangsu.gov.cn/pub/jszfcg/cgxx/cggg/201611/t20161114_105870.html'
    url = 'http://www.ccgp-jiangsu.gov.cn/pub/jszfcg/cgxx/cggg/201611/t20161117_106566.html'
    # url = 'http://www.ccgp-jiangsu.gov.cn/pub/jszfcg/cgxx/cggg/201611/t20161114_105966.html'
    # url = 'http://www.ccgp-jiangsu.gov.cn/pub/jszfcg/cgxx/cggg/201611/t20161117_106517.html'
    # url = 'http://www.gdgpo.gov.cn/showNotice/id/40288ba95801392e015804cebc0529b7.html'
    # url = 'http://www.hebgc.com/hebgc2009/?a=eng-pub-detail&xh=363005'
    # url = 'http://www.zzgp.gov.cn/newsShow.asp?id=13351'
    # url = 'http://ztb.hainan.gov.cn/data/zbgg/2016/11/14088/'
    # url = "http://www.zgazxxw.com/zbpd/zhongbgg/201610/2379408.php"
    # url = 'http://www.gzzbw.cn/html/zbgg/gczb/20161116/217920.html'
    # url = 'http://zb.cbi360.net/tb/20161129/10114775.html'
    # url = 'http://www.gzzbw.cn/html/zbgg/zbgs/2016/1206/221218.html'
    # url = 'http://www.gsei.com.cn/html/1337/2016-11-28/content-148864.html'
    # url = 'http://www.jlsggzyjy.gov.cn/jlsztb/InfoDetail/?InfoID=bfd80159-4c11-4a97-8978-31f02c54e92c&CategoryNum=003001004001'
    # url = 'http://www.cqzb.gov.cn/zbgg-5-67004-2.aspx'
    # url = 'http://cgb.yantai.gov.cn/art/2016/6/13/art_5805_11626.html'

    if len(sys.argv) > 1:
        url = sys.argv[1]

    from_url = 1
    if from_url:
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8,gb2312,GBK;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
    else:
        f = open('te.html', 'r')

    text = f.read().strip()
    if isinstance(text, str) and from_url:
        if 'charset=gb' in text or 'charset="GB' in text or 'charset="UTF' in text:
            try:
                text = text.decode('gbk', 'ignore')
            except:
                pass
        else:  # if 'charset=utf-8' in text or 'charset="UTF-8' in text:
            try:
                text = text.decode('utf-8', 'ignore')
            except:
                pass
    return url, text


if __name__ == '__main__':
    import time

    url, text = test()
    # print text

    table_parser = HTMLTableParser('./keys.txt')

    start = time.time()
    tbs = table_parser.parse(text)
    # print time.time() - start
    ##descs = tbs[1]
    ##tbs = tbs[0]

    count = 0
    # for desc, tb in zip(descs, tbs):
    desc = ''
    for tb in tbs:
        count += 1
        if DEBUG:
            print 'table', count, desc
            for row in tb:
                print '|'.join(row)
            print

    if not DEBUG:
        jsoned = json.dumps({url: tbs}, ensure_ascii=False, encoding='utf-8')
        print jsoned
