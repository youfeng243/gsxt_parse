#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence 
@file: queue_mq_thread.py
@time: 2016/12/8 13:45
"""
import time

from beanstalkc import SocketError
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport.TTransport import TMemoryBuffer

from common.pybeanstalk import PyBeanstalk
from thriftRPC.entity_extractor.ttypes import EntityExtractorInfo

__all__ = ['EntityExtractorInfo']


class MqQueueThread(object):
    PAUSE_COUNT_LV1 = 1000
    PAUSE_COUNT_LV2 = 10000
    PAUSE_COUNT_LV3 = 50000
    PAUSE_COUNT_LV4 = 100000
    PAUSE_COUNT_LV5 = 1000000

    PAUSE_TIME_LV1 = 1
    PAUSE_TIME_LV2 = 3
    PAUSE_TIME_LV3 = 10
    PAUSE_TIME_LV4 = 20
    PAUSE_TIME_LV5 = 300

    def __init__(self, server_conf=None, log=None):
        # threading.Thread.__init__(self)
        # self.daemon = True

        self.log = log

        # 判断是否消息队列已中断
        # self.is_connect = True

        # 判断是否需要暂停
        self.is_pause = False
        self.pause_time = self.PAUSE_TIME_LV1

        # 输送队列
        # self.queue = Queue()

        # 获取消息队列配置
        self.server_conf = server_conf

        # 消息队列
        self.beanstalk = PyBeanstalk(self.server_conf['host'], self.server_conf['port'])
        self.output_tube = self.server_conf['tube']

        # 当前消费长度
        self.length = 0

    def __del__(self):
        self.log.info('消息队列线程退出...')

    # 判断是否需要暂停
    def is_need_pause(self):
        try:
            count = self.beanstalk.get_tube_count(self.output_tube)
        except Exception as e:
            self.log.error('获取当前队列数目失败..开启消息队列休眠...')
            self.log.exception(e)
            count = self.PAUSE_COUNT_LV1

        if count < self.PAUSE_COUNT_LV1:
            self.is_pause = False
            self.pause_time = self.PAUSE_TIME_LV1
            return

        self.is_pause = True
        if count >= self.PAUSE_COUNT_LV5:
            self.pause_time = self.PAUSE_TIME_LV5
        elif count >= self.PAUSE_COUNT_LV4:
            self.pause_time = self.PAUSE_TIME_LV4
        elif count >= self.PAUSE_COUNT_LV3:
            self.pause_time = self.PAUSE_TIME_LV3
        elif count >= self.PAUSE_COUNT_LV2:
            self.pause_time = self.PAUSE_TIME_LV2
        else:
            self.pause_time = self.PAUSE_TIME_LV1

        # 开始休眠
        time.sleep(self.pause_time)

    def push_sync_msg(self, entity_extract_data):
        self.length += 1
        if self.length % 100 == 0:
            self.is_need_pause()

        if self.length >= 10000:
            self.length = 0

        # 序列化数据
        obj_str = self.__to_string(entity_extract_data)
        if obj_str is None:
            return False

        try:
            self.beanstalk.put(self.output_tube, obj_str)
        except SocketError as e:
            self.beanstalk.reconnect()
            time.sleep(10)
            self.log.warn("reconnect beanstalk...")
            self.log.exception(e)
            return False

        except Exception as e:
            self.log.error('捕获异常休眠...')
            self.log.exception(e)
            time.sleep(10)
            return False

        return True

    # def push_msg(self, entity_extract_data):
    #
    #     # 减缓发送消息速度
    #     while not self.is_connect:
    #         self.log.info('消息队列断开连接, 线程休眠20s...')
    #         time.sleep(20)
    #
    #     # 判断是否需要暂停
    #     if self.is_pause:
    #         self.log.info('消息队列堆积, 需要暂停灌入...休眠{pause}s...'.format(
    #             pause=self.pause_time))
    #         time.sleep(self.pause_time)
    #
    #     obj_str = self.__to_string(entity_extract_data)
    #     if obj_str is None:
    #         return
    #
    #     self.queue.put_nowait(obj_str)

    # def close(self):
    #     self.queue.put_nowait('@@##$$')
    #     self.log.info('发送线程退出指令...')

    def __to_string(self, obj):
        str_parse = None
        try:
            memory_b = TMemoryBuffer()
            t_binary_protocol_b = TBinaryProtocol(memory_b)
            obj.write(t_binary_protocol_b)
            str_parse = memory_b.getvalue()
        except EOFError as e:
            self.log.exception(e)
        return str_parse

        # def run(self):
        #     self.log.info('开始运行消息队列...')
        #
        #     while True:
        #         try:
        #             msg = self.queue.get()
        #             if msg == '@@##$$':
        #                 break
        #
        #             while True:
        #                 try:
        #                     self.length += 1
        #                     self.beanstalk.put(self.output_tube, msg)
        #
        #                     # 没完成一百个就判断一下是否需要休眠
        #                     if self.length % 100 == 0:
        #                         self.is_need_pause()
        #
        #                     # 设置消息队列连接状态
        #                     self.is_connect = True
        #                     break
        #                 except SocketError as e:
        #                     # 设置当前消息队列已中断, 减缓发送数据速度
        #                     self.is_connect = False
        #                     time.sleep(10)
        #                     self.beanstalk.reconnect()
        #                     self.log.warn("reconnect beanstalk...")
        #                     self.log.exception(e)
        #                 except Exception as e:
        #                     self.is_connect = False
        #                     self.log.error('捕获异常休眠...')
        #                     self.log.exception(e)
        #                     time.sleep(10)
        #         except Exception as e:
        #             self.log.info('当前队列大小: size = {size}'.format(size=self.queue.qsize()))
        #             self.log.exception(e)
        #             time.sleep(5)
        #
        #     self.log.info('消息队列线程正常退出.')
