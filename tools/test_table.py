#!/usr/bin/env python
# encoding: utf-8

from pyquery import PyQuery

# with open('表格特殊案例1.txt') as p_file:
#     lines = p_file.read().decode(encoding='utf-8')
#     pq = PyQuery(lines, parser='html')
#     for item_table in pq('table').items():
#
#         # print item_table.length
#         # print item_table.children().length
#         print item_table.is_('table')
#         for item in item_table.children().items():
#             print item.children().eq(0).is_('tr')
#             print item.text()
# print item.length
# print item.children().length
# for child_item in item.items():
# print child_item
# print child_item.text()
# print BeautifulSoup(str(child_item), 'lxml').name
# print ''
# print pq.text()

with open('嵌套表格.html') as p_file:
    lines = p_file.read().decode(encoding='utf-8')
    pq = PyQuery(lines, parser='html')
    table_list = pq.find('table')
    #print table_list.length
    table_result = []
    result = ''
    for table in table_list.items():
        # if table.is_('table'):
        #     print '是table'
        # if table.find('table').length > 0:
        #     print '内嵌table'
        # else:
        #     table_result.append(table)
        # print '1111'
        # print table.outer_html()
        if table.find('table').length > 0:
            continue
        result += table.outer_html()

    # print result
    table_list = PyQuery(result, parser='html').find('table')

    print table_list.length
    for item in table_list.items():
        print item.text()
    print '###################'
    del table_list[0]
    print table_list.length
    for item in table_list.items():
        print item.text()
    print '###################'
    del table_list[0]
    print table_list.length
    for item in table_list.items():
        print item.text()
    print '###################'

    # for table in table_list.items():
    #     # print table.length
    #     # print table.is_('table')
    #     #
    #     # print table.next().length
    #     # print table.next().is_('table')
    #     #
    #     # print table.next().next().length
    #     # print table.next().next().is_('table')
    #     print table.parent().length
    #     print table.parent().parent().length
    #     print table.parent().parent().parent().length
    #     break

    # table = table_list
    # print table.length
    # print table.is_('table')
    # # print table_list.outer_html()
    # table = table_list.next()
    # print table.length
    # print table.is_('table')
    #
    # # print table_list.next().outer_html()
    # table = table_list.next().next()
    # print table.length
    # print table.is_('table')
    #
    # table = table_list.next().next().next()
    # print table.length
    # print table.is_('table')
    # if table_list.next().next() is None:
    #     print 'next next is None'

    # for item in PyQuery(result, parser='html').find('table').items():
    #     print '111'
    #     print item.outer_html()
    #
    # parent = table.parent()
    # for item in parent.items():
    #     print type(item.outer_html())
    #     print len(item.outer_html())
    #     #print item.outer_html()
    #     p = PyQuery(item.outer_html(), parser='html')
    #     print p.outer_html()

    # for table in table_list.items():
    #     print table.outer_html()


    # print len(table_result)
    # for table in table_result:
    #     print table.outer_html()

# with open('表格测试4.txt') as p_file:
#     lines = p_file.read().decode(encoding='utf-8')
#     bs = BeautifulSoup(lines, 'lxml')
#     # print bs
#     table_list = bs.find_all('table')
#     # print len(table_list)
#     for item_table in table_list:
#         print len(item_table)
#         for item in item_table.contents:
#             if isinstance(item, NavigableString):
#                 continue
#             # print item
#             print type(item)
#             if item.name == 'tr':
#                 print 'item = tr'
#                 print item.name
#                 print item.get_text()
#                 print item.prettify()
#                 # print item
#                 # print item.name
#                 # print item.get_text()
#                 # print ''
