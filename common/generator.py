#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence 
@file: generator.py
@time: 2016/12/13 17:03
"""

from parse.parse_anhui_worker import GsxtParseAnHuiWorker
from parse.parse_beijing_worker import GsxtParseBeiJingWorker
from parse.parse_chongqing_worker import GsxtParseChongQingWorker
from parse.parse_fujian_worker import GsxtParseFuJianWorker
from parse.parse_gansu_worker import GsxtParseGanSuWorker
from parse.parse_gsxt_worker import GsxtParseGsxtWorker
from parse.parse_guangdong_worker import GsxtParseGuangDongWorker
from parse.parse_guangxi_worker import GsxtParseGuangXiWorker
from parse.parse_guizhou_worker import GsxtParseGuiZhouWorker
from parse.parse_hainan_worker import GsxtParseHaiNanWorker
from parse.parse_hebei_worker import GsxtParseHeBeiWorker
from parse.parse_heilongjiang_worker import GsxtParseHeiLongJiangWorker
from parse.parse_henan_worker import GsxtParseHeNanWorker
from parse.parse_hubei_worker import GsxtParseHuBeiWorker
from parse.parse_hunan_worker import GsxtParseHuNanWorker
from parse.parse_jiangsu_worker import GsxtParseJiangSuWorker
from parse.parse_jiangxi_worker import GsxtParseJiangXiWorker
from parse.parse_jilin_worker import GsxtParseJiLinWorker
from parse.parse_liaoning_worker import GsxtParseLiaoNingWorker
from parse.parse_neimenggu_worker import GsxtParseNeiMengGuWorker
from parse.parse_ningxia_worker import GsxtParseNingXiaWorker
from parse.parse_qinghai_worker import GsxtParseQingHaiWorker
from parse.parse_shandong_worker import GsxtParseShanDongWorker
from parse.parse_shanghai_worker import GsxtParseShangHaiWorker
from parse.parse_shanxi_worker import GsxtParseShanXiWorker
from parse.parse_shanxicu_worker import GsxtParseShanXiCuWorker
from parse.parse_sichuan_worker import GsxtParseSiChuanWorker
from parse.parse_tianjin_worker import GsxtParseTianJinWorker
from parse.parse_xinjiang_worker import GsxtParseXinJiangWorker
from parse.parse_xizang_worker import GsxtParseXiZangWorker
from parse.parse_yunnan_worker import GsxtParseYunNanWorker
from parse.parse_zhejiang_worker import GsxtParseZheJiangWorker

__all__ = ['GsxtHuNanWorker', 'GsxtShanXiWorker', 'GsxtNingXiaWorker', 'GsxtGuiZhouWorker',
           'GsxtLiaoNingWorker', 'GsxtJiangSuWorker', 'GsxtNeiMengGuWorker', 'GsxtTianJinWorker',
           'GsxtShanXiCuWorker', 'GsxtChongQingWorker', 'GsxtSiChuanWorker', 'GsxtXinJiangWorker',
           'GsxtShangHaiWorker', 'GsxtFuJianWorker', 'GsxtGuangDongWorker', 'GsxtBeiJingWorker',
           'GsxtHeiLongJiangWorker', 'GsxtAnHuiWorker', 'GsxtShanDongWorker', 'GsxtGuangXiWorker',
           'GsxtXiZangWorker', 'GsxtQingHaiWorker', 'GsxtHuBeiWorker', 'GsxtHeNanWorker',
           'GsxtHaiNanWorker', 'GsxtGanSuWorker',
           'GsxtDetailAnHuiWorker',
           'GsxtDetailLiaoNingWorker', 'GsxtDetailShanXiCuWorker', 'GsxtDetailShanDongWorker',
           'GsxtDetailBeiJingWorker', 'GsxtDetailXiZangWorker', 'GsxtDetailQingHaiWorker',
           'GsxtDetailHeiLongJiangWorker', 'GsxtDetailHeNanWorker', 'GsxtDetailHuBeiWorker',
           'GsxtHeBeiWorker', 'GsxtYunNanWorker', 'GsxtSearchListBeiJingWorker', 'GsxtSearchListShangHaiWorker',
           'GsxtSearchListGuangDongWorker', 'GsxtSearchListAnHuiWorker', 'GsxtDetailShangHaiWorker',
           'GsxtDetailGuangDongWorker',
           'GsxtSearchListLiaoNingWorker', 'GsxtSearchListShanDongWorker', 'GsxtSearchListShanXiCuWorker',
           'GsxtSearchListFuJianWorker', 'GsxtDetailFuJianWorker', 'GsxtSearchListHeNanWorker',
           'GsxtDetailHuNanWorker', 'GsxtSearchListHuNanWorker', 'GsxtSearchListHuBeiWorker',
           'GsxtSearchListTianJinWorker', 'GsxtSearchListHeBeiWorker', 'GsxtSearchListNeiMengGuWorker',
           'GsxtJiLinWorker', 'GsxtSearchListJiLinWorker', 'GsxtSearchListHeiLongJiangWorker',
           'GsxtSearchListJiangSuWorker', 'GsxtZheJiangWorker', 'GsxtSearchListZheJiangWorker',
           'GsxtJiangXiWorker', 'GsxtSearchListGuangXiWorker', 'GsxtSearchListHaiNanWorker',
           'GsxtSearchListJiangXiWorker', 'GsxtSearchListChongQingWorker', 'GsxtSearchListSiChuanWorker',
           'GsxtSearchListGuiZhouWorker', 'GsxtSearchListYunNanWorker', 'GsxtSearchListXiZangWorker',
           'GsxtSearchListShanXiWorker', 'GsxtSearchListGanSuWorker', 'GsxtSearchListQingHaiWorker',
           'GsxtSearchListNingXiaWorker', 'GsxtSearchListXinJiangWorker', 'GsxtDetailJiangSuWorker',
           'GsxtDetailZheJiangWorker', 'GsxtDetailSiChuanWorker', 'GsxtDetailJiangXiWorker',
           'GsxtDetailTianJinWorker', 'GsxtDetailShanXiWorker', 'GsxtDetailChongQingWorker',
           'GsxtDetailYunNanWorker', 'GsxtDetailHeBeiWorker', 'GsxtDetailXinJiangWorker',
           'GsxtDetailGuiZhouWorker', 'GsxtDetailGuangXiWorker', 'GsxtDetailHaiNanWorker',
           'GsxtDetailGanSuWorker', 'GsxtDetailJiLinWorker', 'GsxtDetailNeiMengGuWorker',
           'GsxtDetailNingXiaWorker', 'GsxtParseAnHuiWorker', 'GsxtParseBeiJingWorker', 'GsxtParseChongQingWorker',
           'GsxtParseFuJianWorker', 'GsxtParseGanSuWorker', 'GsxtParseGuangDongWorker', 'GsxtParseGuangXiWorker',
           'GsxtParseGuiZhouWorker', 'GsxtParseHaiNanWorker', 'GsxtParseHeBeiWorker', 'GsxtParseHeiLongJiangWorker',
           'GsxtParseHeNanWorker', 'GsxtParseHuBeiWorker', 'GsxtParseHuNanWorker', 'GsxtParseJiangSuWorker',
           'GsxtParseJiangXiWorker', 'GsxtParseJiLinWorker', 'GsxtParseLiaoNingWorker', 'GsxtParseNeiMengGuWorker',
           'GsxtParseNingXiaWorker', 'GsxtParseQingHaiWorker', 'GsxtParseShanDongWorker', 'GsxtParseShangHaiWorker',
           'GsxtParseShanXiWorker', 'GsxtParseShanXiCuWorker', 'GsxtParseSiChuanWorker', 'GsxtParseTianJinWorker',
           'GsxtParseXinJiangWorker', 'GsxtParseXiZangWorker', 'GsxtParseYunNanWorker', 'GsxtParseZheJiangWorker',
           'GsxtParseGsxtWorker',
           ]


def create_crawl_object(config_dict, province):
    clazz = config_dict.get('clazz', '')
    if clazz == '':
        raise StandardError("no worker for {province}".format(province=province))

    return eval(clazz)(**config_dict)
