# -*- coding:utf-8 -*-

'''
  # 结构信息
  {
      # 公司名称
      _id:xxx,
      # 种子信息
      seed: xxx,
      # 入库时间
      in_time: '2016-12-17 22:58:36',
      # 站点信息
      province: xizang,
      # 具体数据
      datalist:
              {
                  base_info:{
                   list: [{url:xxx, text:xxx}],
                   detail: [{url:xxx, text:xxx}]
                  },

                  change_info:{
                   list: [{url:xxx, text:xxx}],
                   detail: [{url:xxx, text:xxx}]
                  },
              }
  }
  '''


# 自定义字段缺失异常
class FieldMissError(Exception):
    pass


# 全部属性字段抓取失败
class PageCrawlError(Exception):
    pass


# 部分属性页面抓取失败
# class PartPageCrawlError(Exception):
#     pass


class Model(object):
    # 分类信息
    type_list = 'list'
    type_detail = 'detail'

    # 基本信息
    # base_info: {list:[{url:xxx, text:xxx}], detail:[{url:xxx, text:xxx}]}
    base_info = 'base_info'

    # 股东信息   页面第二项
    # shareholder_info: {list:[{url:xxx, text:xxx}], detail:[{url:xxx, text:xxx}]}
    shareholder_info = 'shareholder_info'

    # 变更信息
    # change_info: {list:[{url:xxx, text:xxx}], detail:[{url:xxx, text:xxx}]}
    change_info = 'change_info'

    # 主要人员
    # key_person_info: {list:[{url:xxx, text:xxx}], detail:[{url:xxx, text:xxx}]}
    key_person_info = 'key_person_info'

    # 分支机构
    # branch_info: {list:[{url:xxx, text:xxx}], detail:[{url:xxx, text:xxx}]}
    branch_info = 'branch_info'

    # 出资信息 或者 股东及出资信息  页面第一项
    # contributive_info: {list:[{url:xxx, text:xxx}], detail:[{url:xxx, text:xxx}]}
    contributive_info = 'contributive_info'

    # 清算信息
    # liquidation_info: {list:[{url:xxx, text:xxx}], detail:[{url:xxx, text:xxx}]}
    liquidation_info = "liquidation_info"

    # 动产抵押登记信息
    chattel_mortgage_info = 'chattel_mortgage_info'

    # 列入经营异常名录信息
    abnormal_operation_info = 'abnormal_operation_info'

    # 股权出质登记信息 股权出资登记
    equity_pledged_info = 'equity_pledged_info'

    # 股权变更信息
    change_shareholding_info = 'change_shareholding_info'

    # 企业年报
    annual_info = "annual_info"
