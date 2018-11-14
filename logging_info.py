#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/13 09:56
__author__ = Kexin Xu
__desc__ = 用logging代替print输出信息
           参考(转载)自: https://blog.csdn.net/Chelydra/article/details/79850366
           侵删
"""

import logging

class LogginInfo():
    """在网上找到的类,防止logging重复记录
    
    """


    def __init__(self, if_write_logs=False, logFilename=r'e:\temp\myLog.log'):

        # 这个设置还需要在理解一下
        logging.basicConfig(
            level=logging.DEBUG, # 定义输出到文件的log级别
            format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s', # 定义输出log的格式
            datefmt='%Y-%m-%d %H:%M:%S', # 时间
            filename=logFilename, # log文件名
            filemode='w')

        self.logger = logging.getLogger(__name__)
        # 以下三行为清空上次文件
        # 这为清空当前文件的logging 因为logging会包含所有的文件的logging
        logging.Logger.manager.loggerDict.pop(__name__)
        # 将当前文件的handlers 清空
        self.logger.handlers = []
        # 然后再次移除当前文件logging配置
        self.logger.removeHandler(self.logger.handlers)

        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if if_write_logs and not self.logger.handlers:
            # loggger 文件配置路径
            self.file_handler = logging.FileHandler(logFilename, encoding='utf-8')
            self.stream_handler = logging.StreamHandler()
        # logger 配置等级
        self.logger.setLevel(logging.DEBUG)
        # logger 输出格式
        file_formatter = logging.Formatter('%(asctime)s %(threadName)s_%(thread)d  %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        # 添加输出格式进入handler
        self.file_handler.setFormatter(file_formatter)
        self.stream_handler.setFormatter(file_formatter)
        # 添加文件设置如handler
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    # 以下皆为重写方法 并且每次记录后清除logger
    def info(self, message=None):
        """logging.info
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.info(message)
        self.logger.removeHandler(self.logger.handlers)

    def debug(self, message=None):
        """logging.debug
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.debug(message)
        self.logger.removeHandler(self.logger.handlers)

    def warning(self, message=None):
        """logging.warning
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.warning(message)
        self.logger.removeHandler(self.logger.handlers)

    def error(self, message=None):
        """logging.error
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.error(message)
        self.logger.removeHandler(self.logger.handlers)

    def critical(self, message=None):
        """logging.critical
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.critical(message)
        self.logger.removeHandler(self.logger.handlers)


class LogginInfoOnlyStream():
    """只使用logging打印url
    
    """


    def __init__(self):

        self.logger = logging.getLogger(__name__)
        logging.Logger.manager.loggerDict.pop(__name__)
        self.logger.handlers = []
        self.logger.removeHandler(self.logger.handlers)
        self.logger.setLevel(logging.DEBUG)
        # logger 输出格式
        file_formatter = logging.Formatter('%(asctime)s  %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        if not self.logger.handlers:
            # loggger 文件配置路径
            self.stream_handler = logging.StreamHandler()

        # 添加输出格式进入handler
        self.stream_handler.setFormatter(file_formatter)
        # 添加文件设置如handler
        self.logger.addHandler(self.stream_handler)

    # 以下皆为重写方法 并且每次记录后清除logger
    def info(self, message=None):
        """logging.info
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.info(message)
        self.logger.removeHandler(self.logger.handlers)

    def debug(self, message=None):
        """logging.debug
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.debug(message)
        self.logger.removeHandler(self.logger.handlers)

    def warning(self, message=None):
        """logging.warning
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.warning(message)
        self.logger.removeHandler(self.logger.handlers)

    def error(self, message=None):
        """logging.error
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.error(message)
        self.logger.removeHandler(self.logger.handlers)

    def critical(self, message=None):
        """logging.critical
        
        Parameters
        ----------
        message : str, optional
            打印的信息 (the default is None, which None)
        
        """

        self.__init__()
        self.logger.critical(message)
        self.logger.removeHandler(self.logger.handlers)



# def console_log_debug(pic_name, url, logFilename):
#     """打印程序的log,使用debug方式
    
#     Parameters
#     ----------
#     url : str
#         pic网址
#     pic_name : str
#         pic名称
#     logFilename : str
#         log的保存路径
    
#     """
#     logger = logging.getLogger('pic_log')

#     logging.basicConfig(
#         level=logging.DEBUG, # 定义输出到文件的log级别
#         format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s', # 定义输出log的格式
#         datefmt='%Y-%m-%d %H:%M:%S', # 时间
#         filename=logFilename, # log文件名
#         filemode='w')

#     # 定义console handler, Strem不影响输出的文件
#     console = logging.StreamHandler()
#     # 定义该handler级别
#     console.setLevel(logging.INFO) 
#     #定义该handler格式
#     fmt = logging.Formatter('%(asctime)s %(threadName)s_%(thread)d  %(message)s',
#                             datefmt='%Y-%m-%d %H:%M:%S')
#     # fmt = logging.Formatter('%(message)s')
#     console.setFormatter(fmt)

#     logging.getLogger().addHandler(console) # 实例化添加handler

#     logging.debug(pic_name + ' ' + url)
#     logger.removeHandler(console)
    

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


# 级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
# DEBUG : 打印全部的日志,详细的信息,通常只出现在诊断问题上
# INFO : 打印info,warning,error,critical级别的日志,确认一切按预期运行
# WARNING : 打印warning,error,critical级别的日志,一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”),这个软件还能按预期工作
# ERROR : 打印error,critical级别的日志,更严重的问题,软件没能执行一些功能
# CRITICAL : 打印critical级别,一个严重的错误,这表明程序本身可能无法继续运行
