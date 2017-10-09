#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence 
@file: signal_test.py
@time: 2017/2/28 12:15
"""
import signal
import time

is_running = True


def onSigInt(signo, frame):
    global is_running
    print 'onSigInt {signo}'.format(signo=signo)
    is_running = False


def onSigTerm(signo, frame):
    global is_running
    print 'onSigTerm {signo}'.format(signo=signo)
    is_running = False


def test():
    global is_running
    while is_running:
        time.sleep(1)
        print "."
    print "App exit gracefully."


if __name__ == "__main__":
    # 主进程退出信号
    signal.signal(signal.SIGINT, onSigInt)
    signal.signal(signal.SIGTERM, onSigTerm)

    test()
