#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence 
@file: gsxt_field.py
@time: 2017/3/8 10:03
"""

# 统一社会信用代码/注册号 辽宁这个如何归类
from common.global_field import FieldMissError


class GsModel:
    def __init__(self):
        pass

    # 企业名称
    COMPANY = u'company'
    # 派出企业名称
    SEND_COMPANY = u'send_company'
    # 转换前的注册资本
    REGISTERED_CAPITAL = u'src_registered_capital'
    # 法定代表人
    LEGAL_MAN = u'legal_man'
    # 法定代表人字段类型
    LEGAL_MAN_TYPE = u'legal_man_type'
    # 类型
    ENTERPRISE_TYPE = u'enterprise_type'
    # 成立日期
    REGISTERED_DATE = u'registered_date'
    # 吊销日期
    REVOCATION_DATE = u'revocation_date'
    # 注销日期
    CANCEL_DATE = u'cancel_date'
    # 营业期限自
    PERIOD_FROM = u'period_from'
    # 营业期限至
    PERIOD_TO = u'period_to'
    # 营业周期
    PERIOD = u'period'
    # 登记机关
    REGISTERED_ADDRESS = u'registered_address'
    # 核准日期
    HEZHUN_DATE = u'hezhun_date'
    # 登记状态
    BUSINESS_STATUS = u'business_status'
    # 住所
    ADDRESS = u'address'
    # 经营范围
    BUSINESS_SCOPE = u'business_scope'
    # CODE,用来处理中间结果字段统一社会信用号或者注册号
    CODE = u'code'

    # 企业联系电话
    CONTACT_NUMBER = u'contact_number'

    # 邮政编码
    ZIP_CODE = u'zip_code'

    # 统一社会信用代码
    UNIFIED_SOCIAL_CREDIT_CODE = u'unified_social_credit_code'
    # 注册号
    REGISTERED_CODE = u'registered_code'

    # 省份
    PROVINCE = u'province'

    # 股票代码
    STOCK_CODE = u'stock_code'

    # 迁入地工商局
    SETTLE_IN_INSTITUTION = u"settle_in_institution"

    # 组成形式
    COMPOSING_FORM = u'composing_form'

    # 主要人员
    KEY_PERSON = u'key_person'

    class KeyPerson:
        def __init__(self):
            pass

        KEY_PERSON_NAME = u'key_person_name'
        KEY_PERSON_POSITION = u'key_person_position'

    # 工商变更信息
    CHANGERECORDS = u'changerecords'

    class ChangeRecords:
        def __init__(self):
            pass

        CHANGE_DATE = u'change_date'
        AFTER_CONTENT = u'after_content'
        BEFORE_CONTENT = u'before_content'
        CHANGE_ITEM = u'change_item'

    # 分支机构
    BRANCH = u'branch'

    class Branch:
        def __init__(self):
            pass

        COMPAY_NAME = u'compay_name'
        REGISTERED_CODE = u'registered_code'
        # 新增
        CODE = u'code'
        TYPE = u'type'
        # 新增
        REGISTERED_ADDRESS = u'registered_address'

    # 出资人信息列表
    CONTRIBUTOR_INFORMATION = u'contributor_information'

    class ContributorInformation:
        def __init__(self):
            pass

        SHAREHOLDER_NAME = u'shareholder_name'
        SHAREHOLDER_TYPE = u'shareholder_type'
        SUBSCRIPTION_AMOUNT = u'subscription_amount'
        CERTIFICATE_TYPE = u'certificate_type'
        CERTIFICATE_NO = u'certificate_no'
        PAIED_AMOUNT = u'paied_amount'
        # PAIED_AMOUNT_UNIT = u'paied_amount_unit'
        # SUBSCRIPTION_AMOUNT_UNIT = u'subscription_amount_unit'
        SUBSCRIPTION_DETAIL = u'subscription_detail'

        # 认缴
        class SubscriptionDetail:
            def __init__(self):
                pass

            SUBSCRIPTION_TYPE = u'subscription_type'
            SUBSCRIPTION_TIME = u'subscription_time'
            SUBSCRIPTION_AMOUNT = u'subscription_amount'
            # SUBSCRIPTION_AMOUNT_UNIT = u'subscription_amount_unit'
            SUBSCRIPTION_PUBLISH_TIME = u'subscription_publish_time'

        PAIED_DETAIL = u'paied_detail'

        # 实缴
        class PaiedDetail:
            def __init__(self):
                pass

            PAIED_AMOUNT = u'paied_amount'
            PAIED_TIME = u'paied_time'
            PAIED_TYPE = u'paied_type'
            # PAIED_AMOUNT_UNIT = u'paied_amount_unit'
            PAIED_PUBLISH_TIME = u'paied_publish_time'

    # 股东信息
    SHAREHOLDER_INFORMATION = u'shareholder_information'

    class ShareholderInformation:
        def __init__(self):
            pass

        SHAREHOLDER_NAME = u'shareholder_name'
        SHAREHOLDER_TYPE = u'shareholder_type'
        # 认缴
        SUBSCRIPTION_AMOUNT = u'subscription_amount'
        SUBSCRIPTION_TYPE = u'subscription_type'
        SUBSCRIPTION_TIME = u'subscription_time'
        # SUBSCRIPTION_AMOUNT_UNIT = u'subscription_amount_unit'
        SUBSCRIPTION_PUBLISH_TIME = u'subscription_publish_time'
        # 证件
        CERTIFICATE_TYPE = u'certificate_type'
        CERTIFICATE_NO = u'certificate_no'

        SUBSCRIPTION_DETAIL = u'subscription_detail'

        class SubscriptionDetail:
            def __init__(self):
                pass

            SUBSCRIPTION_TYPE = u'subscription_type'
            SUBSCRIPTION_TIME = u'subscription_time'
            SUBSCRIPTION_AMOUNT = u'subscription_amount'
            # SUBSCRIPTION_AMOUNT_UNIT = u'subscription_amount_unit'
            SUBSCRIPTION_PUBLISH_TIME = u'subscription_publish_time'

        # 实缴
        PAIED_AMOUNT = u'paied_amount'
        PAIED_TYPE = u'paied_type'
        PAIED_TIME = u'paied_time'
        # PAIED_AMOUNT_UNIT = u'paied_amount_unit'
        PAIED_PUBLISH_TIME = u'paied_publish_time'

        PAIED_DETAIL = u'paied_detail'

        class PaiedDetail:
            def __init__(self):
                pass

            PAIED_AMOUNT = u'paied_amount'
            PAIED_TIME = u'paied_time'
            PAIED_TYPE = u'paied_type'
            # PAIED_AMOUNT_UNIT = u'paied_amount_unit'
            PAIED_PUBLISH_TIME = u'paied_publish_time'

    # 动产抵押登记信息
    CHATTEL_MORTGAGE_INFO = u'chattel_mortgage_info'

    class ChattelMortgageInfo(object):
        def __init__(self):
            pass

        # 登记编号
        REGISTER_NUM = u'register_num'

        # 登记日期
        REGISTER_DATE = u'register_date'

        # 登记机关
        REGISTER_OFFICE = u'register_office'

        # 被担保债权数额
        CREDIT_AMOUNT = u'credit_amount'

        # 状态
        STATUS = u'status'

        # 公示日期
        PUBLISH_DATE = u'publish_date'

        # 详情
        CHATTEL_DETAIL = u'chattel_detail'

        # map
        class ChattelDetail(object):
            def __init__(self):
                pass

            # 动产抵押登记信息
            CHATTEL_MORTGAGE = u'chattel_mortgage'

            # map
            class ChattelMortgage(object):
                # 登记编号
                REGISTER_NUM = u'register_num'

                # 登记日期
                REGISTER_DATE = u'register_date'

                # 登记机关
                REGISTER_OFFICE = u'register_office'

            # 抵押权人概况信息
            MORTGAGE_PERSON_STATUS = u'mortgage_person_status'

            # list
            class MortgagePersonStatus(object):
                # 抵押权人名称
                MORTGAGE_PERSON_NAME = u'mortgage_person_name'

                #  抵押权人证照/证件类型
                CERTIFICATE_TYPE = u'certificate_type'

                # 证照/证件号码
                CERTIFICATE_NUM = u'certificate_num'

                # 住所地
                ADDRESS = u'address'

            # 被担保债权概况信息
            GUARANTEED_PERSON_STATUS = u'guaranteed_person_status'

            # map
            class GuaranteedPersonStatus(object):
                # 种类
                KIND = u'kind'
                # 担保的范围
                SCOPE = u'scope'
                # 数额
                AMOUNT = u'amount'
                # 债务人履行债务的期限
                PERIOD = u'period'
                # 备注
                REMARK = u'remark'

            # 抵押物概况信息
            GUARANTEE_STATUS = u'guarantee_status'

            # list
            class GuaranteeStatus(object):
                # 名称
                NAME = u'name'
                # 所有权或使用权归属
                AFFILIATION = u'affiliation'
                # 数量、质量、状况、所在地等情况
                SITUATION = u'situation'
                # 备注
                REMARK = u'remark'

            # 变更信息
            CHANGE_INFO = u'change_info'

            # list
            class ChangeInfo(object):
                # 变更日期
                CHANGE_DATE = u'change_date'
                # 变更内容
                CHANGE_CONTENT = u'change_content'

    # 列入经营异常名录信息
    ABNORMAL_OPERATION_INFO = u'abnormal_operation_info'

    # list
    class AbnormalOperationInfo(object):
        def __init__(self):
            pass

        # 列入经营异常名录原因
        ENROL_REASON = u'enrol_reason'

        # 列入日期
        ENROL_DATE = u'enrol_date'

        # 作出决定机关（列入）
        ENROL_DECIDE_OFFICE = u'enrol_decide_office'

        # 移出经营异常名录原因
        REMOVE_REASON = u'remove_reason'

        # 移出日期
        REMOVE_DATE = u'remove_date'

        # 作出决定机关（移出）
        REMOVE_DECIDE_OFFICE = u'remove_decide_office'

    # 股权出质登记信息 股权出资登记
    EQUITY_PLEDGED_INFO = u'equity_pledged_info'

    # list
    class EquityPledgedInfo(object):
        def __init__(self):
            pass

        # 登记编号
        REGISTER_NUM = u'register_num'

        # 出质人
        MORTGAGOR = u'mortgagor'

        # 证照/证件号码
        MORTGAGOR_NUM = u'mortgagor_num'

        # 出质股权数额
        PLEDGE_STOCK_AMOUNT = u'pledge_stock_amount'

        # 质权人
        PLEDGEE = u'pledgee'

        # 证照/证件号码
        PLEDGEE_NUM = u'pledgee_num'

        # 股权出质设立登记日期
        REGISTER_DATE = u'register_date'

        # 状态
        STATUS = u'status'

        # 公示日期
        PUBLISH_DATE = u'publish_date'

        # 详情
        EQUITY_PLEDGED_DETAIL = u'equity_pledged_detail'

        # map
        class EquityPledgedDetail(object):
            # 变更信息
            CHANGE_INFO = u'change_info'

            # list
            class ChangeInfo(object):
                # 变更日期
                CHANGE_DATE = u'change_date'
                # 变更内容
                CHANGE_CONTENT = u'change_content'

    # 公司提供股权变更信息
    CHANGE_SHAREHOLDING = u'change_shareholding'

    class ChangeShareholding:
        def __init__(self):
            pass

        SHAREHOLDER = u'shareholder'
        # 变更前股权比例
        CHANGE_BEFORE = u'change_before'
        # 变更后股权比例
        CHANGE_AFTER = u'change_after'
        # 股权变更日期
        CHANGE_DATE = u'change_date'
        # 公示日期
        PUBLIC_DATE = u'public_date'

    MAP_BASE_CN2EN = {
        u"企业名称": COMPANY,
        u"名称": COMPANY,
        u"个体户名称": COMPANY,
        u"派出企业名称": SEND_COMPANY,
        u"注册资本": REGISTERED_CAPITAL,
        u"成员出资总额": REGISTERED_CAPITAL,
        u"注册资金": REGISTERED_CAPITAL,
        u"设备价款": REGISTERED_CAPITAL,

        u"法定代表人": LEGAL_MAN,
        u"法人代表": LEGAL_MAN,
        u"法定代表": LEGAL_MAN,
        u"企业法人": LEGAL_MAN,
        u"投资人": LEGAL_MAN,
        u"负责人": LEGAL_MAN,
        u"首席代表": LEGAL_MAN,
        u"经营者": LEGAL_MAN,
        u"执行事务合伙人": LEGAL_MAN,
        u"法人": LEGAL_MAN,
        u"委派代表": LEGAL_MAN,

        u"类型": ENTERPRISE_TYPE,
        u"成立日期": REGISTERED_DATE,
        u"注册日期": REGISTERED_DATE,
        u"吊销日期": REVOCATION_DATE,
        u"注销日期": CANCEL_DATE,
        u"营业期限自": PERIOD_FROM,
        u"经营期限自": PERIOD_FROM,
        u"合伙期限自": PERIOD_FROM,
        u"经营(驻在)期限自": PERIOD_FROM,
        u"营业期限至": PERIOD_TO,
        u"经营期限至": PERIOD_TO,
        u"合伙期限至": PERIOD_TO,
        u"经营(驻在)期限至": PERIOD_TO,
        u"登记机关": REGISTERED_ADDRESS,
        u"核准日期": HEZHUN_DATE,
        u"登记状态": BUSINESS_STATUS,
        u"住所": ADDRESS,
        u"营业场所": ADDRESS,
        u"经营场所": ADDRESS,
        u"主要经营场所": ADDRESS,
        u"地址": ADDRESS,
        u"企业通信地址": ADDRESS,
        u"驻在场所": ADDRESS,

        u"经营范围": BUSINESS_SCOPE,
        u"业务范围": BUSINESS_SCOPE,
        u"统一社会信用代码": UNIFIED_SOCIAL_CREDIT_CODE,
        u'统一社会信用代码/注册号': CODE,
        u'注册号/统一社会信用代码': CODE,
        u'注册号': REGISTERED_CODE,
        u'营业执照注册号': REGISTERED_CODE,

        u"省份": PROVINCE,
        u"迁入地工商局": SETTLE_IN_INSTITUTION,

        u"组成形式": COMPOSING_FORM,

        u"企业联系电话": CONTACT_NUMBER,
        u"邮政编码": ZIP_CODE,

    }

    @staticmethod
    def format_base_model(k):
        key = GsModel.MAP_BASE_CN2EN.get(k)
        if key is None:
            raise FieldMissError('基本信息字段 {key} 映射失败'.format(key=k))

        return key

    @staticmethod
    def get_md5_key_position(some_md5):
        switch = {
            # md5 k  : value
            "4c4210b839b704a2a04434287f9ddcf7": u'执行董事',
            "a9bf7fba0080657693bf789e96924818": u'董事长',
            "0d660ca7fa1612075cb83e689086af90": u'监事',
            "b4729d80e2e178b6d75ab58d164533b6": u'董事',
            "f77eecce79e439a35959d202b65075e9": u'总经理',
            "8bfacc3dc52dcd9018cb49f2b478b4ea": u'经理',
            "cbd50d172b8a6562f4afcc75090bca46": u'首席代表',
            "56f69ee518c98ba3db1ba779f2c2e642": u'负责人',
            "f94cb7d9c4da75095a814e38ad0c3365": u'监事',
            "47eda3346de8b5c15e8376386c751150": u'其他人员',
            "33671ceca8c11d12b8b2f36c805b6e6e": u'厂长',
            "c59858aa5d07fbe17b155ec964f3b26c": u'副总经理',
            '110998e87741a0067535b4db59cc4833': u'董事兼总经理',
            '3c0c98a687aeed0fe1884c5ddc71c0a5': u'独立董事',
            '28f1da6ef0b12acc53c9307e8a8ce7a3': u'副董事长',
            '20ba823388cbc351325a999da2269dec': u'监事会主席',
        }
        if some_md5 not in switch:
            raise FieldMissError(u"没有映射: {md5}".format(md5=some_md5))

        return switch[some_md5]
