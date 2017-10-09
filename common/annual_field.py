#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence 
@file: annual_field.py
@time: 2017/3/8 10:02
"""

# 年报model
from common.global_field import FieldMissError


class AnnualReports:
    def __init__(self):
        pass

    # # todo 年报就只有一个号如何处理
    # UNIFIED_SOCIAL_CREDIT_CODE = u'unified_social_credit_code'

    # 统一社会信用代码
    CODE = u'code'

    # 企业主营业务活动
    BUSINESS_ACTIVITIES = u'business_activities'

    # 隶属企业统一社会信用代码/注册号
    SUPER_CODE = u'super_code'

    # 隶属企业名称
    SUPER_COMPANY = u'super_company'

    # 法定代表人
    LEGAL_MAN = u'legal_man'
    # 注册资本
    REGISTERED_CAPITAL = u'src_registered_capital'
    # 企业名称
    COMPANY_NAME = u'company_name'
    # 企业联系电话
    CONTACT_NUMBER = u'contact_number'
    # 邮政编码
    ZIP_CODE = u'zip_code'

    # 经营状态
    BUSINESS_STATUS = u'business_status'
    # 从业人数
    EMPLOYED_POPULATION = u'employed_population'
    # 女性从业人数
    EMPLOYED_POPULATION_WOMAN = u'employed_population_woman'
    # 成员人数中农民人数
    EMPLOYED_POPULATION_FARMER = u'employed_population_farmer'
    # 本年度新增成员人数
    EMPLOYED_POPULATION_INCREASED = u'employed_population_increased'
    # 本年度退出成员人数
    EMPLOYED_POPULATION_QUIT = u'employed_population_quit'
    # 企业控股情况
    ENTERPRISE_HOLDING = u'enterprise_holding'
    EMAIL = u'email'
    # 企业通信地址
    ADDRESS = u'address'
    # 企业经营场所
    BUSINESS_SITE = u'business_site'
    # 企业是否有投资信息或购买其他公司股权
    IS_INVEST = u'is_invest'
    # 是否有网站
    IS_WEB = u'is_web'
    # 是否股权转让
    IS_TRANSFER = u'is_transfer'
    # 是否提供对外担保
    IS_OUT_GUARANTEE = u'is_out_guarantee'
    # 主体类型
    PRINCIPAL_TYPE = u'principal_type'

    # 站点信息
    WEBSITES = u'websites'

    class WebSites:
        def __init__(self):
            pass

        TYPE = u'type'
        NAME = u'name'
        SITE = u'site'

    # 行政许可信息
    ADMIN_LICENSE_INFO = u'administrative_licensing_info'

    class AdminLicenseInfo:
        def __init__(self):
            pass

        LICENSE_NAME = u'license_name'
        LICENSE_PERIOD_DATE = u'license_period_date'

    # 股东出资
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
        # 证件
        CERTIFICATE_TYPE = u'certificate_type'
        CERTIFICATE_NO = u'certificate_no'
        # 实缴
        PAIED_AMOUNT = u'paied_amount'
        PAIED_TYPE = u'paied_type'
        PAIED_TIME = u'paied_time'
        # PAIED_AMOUNT_UNIT = u'paied_amount_unit'

    # 对外投资信息
    INVESTED_COMPANIES = u'invested_companies'

    # todo 还需要和思亮沟通那边如何处理
    class InvestedCompanies:
        def __init__(self):
            pass

        COMPANY_NAME = u'company_name'
        REGISTERED_CODE = u'registered_code'
        UNIFIED_SOCIAL_CREDIT_CODE = u'unified_social_credit_code'
        CODE = u'code'

    # 分支机构
    BRANCH_INFO = u'branch_info'

    class BranchInfo:
        # 分支机构名称
        def __init__(self):
            pass

        BRANCH_NAME = u'branch_name'
        # 分支机构注册号
        BRANCH_CODE = u'branch_code'

    # 企业资产状况
    ENTERPRISE_ASSET_STATUS_INFORMATION = u'enterprise_asset_status_information'

    class EnterpriseAssetStatusInformation:
        # 资产总额
        def __init__(self):
            pass

        GENERAL_ASSETS = u'general_assets'
        # 所有者权益合计
        TOTAL_EQUITY = u'total_equity'
        # 销售总额
        GROSS_SALES = u'gross_sales'
        # 利润总额
        TOTAL_PROFIT = u'total_profit'
        # 营业总收入中主营业务收入
        INCOME_OF_TOTAL = u'income_of_total'
        # 净利润
        RETAINED_PROFITS = u'retained_profits'
        # 纳税总额
        TOTAL_TAX = u'total_tax'
        # 负债总额
        TOTAL_INDEBTEDNESS = u'total_indebtedness'
        # 扶持资金或补助
        FUND_SUBSIDY = u'fund_subsidy'

    # 修改记录
    EDIT_CHANGE_INFOS = u'edit_change_infos'

    class EditChangeInfos:
        def __init__(self):
            pass

        CHANGE_DATE = u'change_date'
        CHANGE_ITEM = u'change_item'
        AFTER_CONTENT = u'after_content'
        BEFORE_CONTENT = u'before_content'

    # 股权变更
    EDIT_SHAREHOLDING_CHANGE_INFOS = u'edit_shareholding_change_infos'

    class EditShareholdingChangeInfos:
        def __init__(self):
            pass

        SHAREHOLDER_NAME = u'shareholder_name'
        AFTER_CONTENT = u'after_content'
        BEFORE_CONTENT = u'before_content'
        CHANGE_DATE = u'change_date'
        PERFORMANCE_PERIOD = u'performance_period'

    # 对外担保信息列表
    OUT_GUARANTEE_INFO = u'out_guarantee_info'

    class OutGuaranteeInfo:
        # 债权人
        def __init__(self):
            pass

        CREDITOR = u'creditor'
        # 债务人
        OBLIGOR = u'obligor'
        # 主债权种类
        DEBT_TYPE = u'debt_type'
        # 主债权金额
        DEBT_AMOUNT = u'debt_amount'
        # 主债权金额单位
        # DEBT_AMOUNT_UNIT = u'debt_amount_unit'
        # 履行债务的期限
        PERFORMANCE_PERIOD = u'performance_period'
        # 担保期间
        GUARANTEE_PERIOD = u'guarantee_period'
        # 担保方式
        GUARANTEE_TYPE = u'guarantee_type'
        # 担保范围
        GUARANTEE_PURVIEW = u'guarantee_purview'

    # todo 后续需要不断补充case
    MAP_BASE_CN2EN = {
        u'统一社会信用代码/注册号': CODE,
        u'统一社会信用代码': CODE,
        u'注册号': CODE,
        u'隶属企业统一社会信用代码/注册号': SUPER_CODE,
        u'注册号/统一社会信用代码': CODE,
        u'隶属企业名称': SUPER_COMPANY,
        u'隶属名称': SUPER_COMPANY,
        u"企业名称": COMPANY_NAME,
        u"个体户名称": COMPANY_NAME,
        u"合作社名称": COMPANY_NAME,
        u'农专社名称': COMPANY_NAME,
        u'名称': COMPANY_NAME,
        u"企业通信地址": ADDRESS,
        u"通信地址": ADDRESS,
        u"企业经营场所": BUSINESS_SITE,
        u"营业场所": BUSINESS_SITE,
        u"邮政编码": ZIP_CODE,
        u"企业联系电话": CONTACT_NUMBER,
        u"经营者联系电话": CONTACT_NUMBER,
        u"联系电话": CONTACT_NUMBER,
        u"企业电子邮箱": EMAIL,
        u"电子邮箱": EMAIL,
        u"电子邮件": EMAIL,
        u"从业人数": EMPLOYED_POPULATION,
        u"成员人数": EMPLOYED_POPULATION,
        u"其中女性从业人数": EMPLOYED_POPULATION_WOMAN,
        u"女性从业人员": EMPLOYED_POPULATION_WOMAN,
        u"企业经营状态": BUSINESS_STATUS,
        u"经营状态": BUSINESS_STATUS,
        u"是否有网站或网店": IS_WEB,
        u"有限责任公司本年度是否发生股东股权转让": IS_TRANSFER,
        u"是否有投资信息或购买其他公司股权": IS_INVEST,
        u"企业是否有投资信息或购买其他公司股权": IS_INVEST,
        u"是否对外提供保证担保信息": IS_OUT_GUARANTEE,
        u"是否有对外提供担保信息": IS_OUT_GUARANTEE,
        u"是否有对外担保信息": IS_OUT_GUARANTEE,
        u"企业主营业务活动": BUSINESS_ACTIVITIES,
        u"主营业务活动": BUSINESS_ACTIVITIES,
        u"企业控股情况": ENTERPRISE_HOLDING,
        u"企业控股": ENTERPRISE_HOLDING,
        u"经营者名称": LEGAL_MAN,
        u"经营者姓名": LEGAL_MAN,
        u"投资人": LEGAL_MAN,
        u"负责人": LEGAL_MAN,
        u'法人代表': LEGAL_MAN,
        u'企业法人': LEGAL_MAN,
        u'执行合伙人': LEGAL_MAN,
        u"资金数额": REGISTERED_CAPITAL,
        u'成员人数中农民人数': EMPLOYED_POPULATION_FARMER,
        u'本年度新增成员人数': EMPLOYED_POPULATION_INCREASED,
        u'本年度退出成员人数': EMPLOYED_POPULATION_QUIT,
        u'主体类型': PRINCIPAL_TYPE,
        u'企业类型': PRINCIPAL_TYPE,
    }

    @staticmethod
    def format_base_model(k):
        key = AnnualReports.MAP_BASE_CN2EN.get(k)
        if key is None:
            raise FieldMissError('基本信息字段 {key} 映射失败'.format(key=k))

        return key

    MAP_ASSET_CN2EN = {
        u"资产总额": EnterpriseAssetStatusInformation.GENERAL_ASSETS,
        u"所有者权益合计": EnterpriseAssetStatusInformation.TOTAL_EQUITY,
        u"营业总收入": EnterpriseAssetStatusInformation.GROSS_SALES,
        u"营业额或营业总收入": EnterpriseAssetStatusInformation.GROSS_SALES,
        u"销售(营业)收入": EnterpriseAssetStatusInformation.GROSS_SALES,
        u"营业额或营业收入": EnterpriseAssetStatusInformation.GROSS_SALES,
        u"销售额或营业收入": EnterpriseAssetStatusInformation.GROSS_SALES,
        u"销售总额": EnterpriseAssetStatusInformation.GROSS_SALES,
        u"利润总额": EnterpriseAssetStatusInformation.TOTAL_PROFIT,
        u"营业总收入中主营业务收入": EnterpriseAssetStatusInformation.INCOME_OF_TOTAL,
        u"销售总额中主营业务收入": EnterpriseAssetStatusInformation.INCOME_OF_TOTAL,
        u"主营业务收入": EnterpriseAssetStatusInformation.INCOME_OF_TOTAL,
        u"其中：主营业务收入": EnterpriseAssetStatusInformation.INCOME_OF_TOTAL,
        u"净利润": EnterpriseAssetStatusInformation.RETAINED_PROFITS,
        u"盈余总额": EnterpriseAssetStatusInformation.RETAINED_PROFITS,
        u"纳税总额": EnterpriseAssetStatusInformation.TOTAL_TAX,
        u'纳税金额': EnterpriseAssetStatusInformation.TOTAL_TAX,
        u"负债总额": EnterpriseAssetStatusInformation.TOTAL_INDEBTEDNESS,
        u"金融贷款": EnterpriseAssetStatusInformation.TOTAL_INDEBTEDNESS,
        u"获得政府扶持资金、补助": EnterpriseAssetStatusInformation.FUND_SUBSIDY,
    }

    @staticmethod
    def format_asset_model(k):
        key = AnnualReports.MAP_ASSET_CN2EN.get(k)
        if key is None:
            raise FieldMissError('企业资产状况字段 {key} 映射失败'.format(key=k))

        return key

    MAP_WEBSITE_CN2EN = {
        u"类型": WebSites.TYPE,
        u"网址": WebSites.SITE,
        u"网站": WebSites.SITE
    }

    @staticmethod
    def format_website_model(k):
        key = AnnualReports.MAP_WEBSITE_CN2EN.get(k)
        if key is None:
            raise FieldMissError('网站网点字段 {key} 映射失败'.format(key=k))

        return key

    MAP_LICENSE_CN2EN = {
        u"许可文件名称": AdminLicenseInfo.LICENSE_NAME,
        u"有效期至": AdminLicenseInfo.LICENSE_PERIOD_DATE,
    }

    @staticmethod
    def format_license_model(k):
        key = AnnualReports.MAP_LICENSE_CN2EN.get(k)
        if key is None:
            raise FieldMissError('行政许可信息字段 {key} 映射失败'.format(key=k))

        return key

    MAP_BRANCH_CN2EN = {
        u"分支机构名称": BranchInfo.BRANCH_NAME,
        u"分支机构注册号": BranchInfo.BRANCH_CODE,
    }

    @staticmethod
    def format_branch_model(k):
        key = AnnualReports.MAP_BRANCH_CN2EN.get(k)
        if key is None:
            raise FieldMissError('分支机构字段 {key} 映射失败'.format(key=k))

        return key
