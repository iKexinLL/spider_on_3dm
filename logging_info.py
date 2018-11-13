#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/13 09:56
__author__ = Kexin Xu
__desc__ = 用logging代替print输出信息
"""

import logging


def console_log(url, pic_name, logFilename):
    """打印程序的log
    
    Parameters
    ----------
    url : str
        pic网址
    pic_name : str
        pic名称
    logFilename : str
        log的保存路径
    
    """

    logging.basicConfig(
        level=logging.DEBUG, # 定义输出到文件的log级别，                                                            
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s', # 定义输出log的格式
        datefmt='%Y-%m-%d %H:%M:%S', # 时间
        filename=logFilename, # log文件名
        filemode='w')

    # 定义console handler
    console = logging.StreamHandler()
    # 定义该handler级别
    console.setLevel(logging.INFO) 
    #定义该handler格式
    fmt = logging.Formatter('%(asctime)s %(threadName)s_%(thread)d  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')                                   
    console.setFormatter(fmt)

    logging.getLogger().addHandler(console) # 实例化添加handler

    logging.info(pic_name + ' ' + url)


    
# class LoggingInfo():

#     def __init__(self):
#         self.log = 

#     @staticmethod
#     def logging_format(format):
#         pass

# StreamHandler：logging.StreamHandler；日志输出到流，可以是sys.stderr，sys.stdout或者文件
# FileHandler：logging.FileHandler；日志输出到文件
# BaseRotatingHandler：logging.handlers.BaseRotatingHandler；基本的日志回滚方式
# RotatingHandler：logging.handlers.RotatingHandler；日志回滚方式，支持日志文件最大数量和日志文件回滚
# TimeRotatingHandler：logging.handlers.TimeRotatingHandler；日志回滚方式，在一定时间区域内回滚日志文件
# SocketHandler：logging.handlers.SocketHandler；远程输出日志到TCP/IP sockets
# DatagramHandler：logging.handlers.DatagramHandler；远程输出日志到UDP sockets
# SMTPHandler：logging.handlers.SMTPHandler；远程输出日志到邮件地址
# SysLogHandler：logging.handlers.SysLogHandler；日志输出到syslog
# NTEventLogHandler：logging.handlers.NTEventLogHandler；远程输出日志到Windows NT/2000/XP的事件日志
# MemoryHandler：logging.handlers.MemoryHandler；日志输出到内存中的指定buffer
# HTTPHandler：logging.handlers.HTTPHandler；通过"GET"或者"POST"远程输出到HTTP服务器
