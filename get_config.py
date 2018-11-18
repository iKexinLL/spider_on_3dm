#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/02 16:05
__author__ = Kexin Xu
__desc__ = 获取设置
    我的想法是通过这个类,来获取设置,以方便后续使用
    而不是将设置放在py文件中.
"""


from configparser import ConfigParser
import os
import datetime

class GetConfig:
    """ 获取程序配置文件

    :return: 返回包含信息的字典
    :rtype: dict
    """

    def __init__(self):
        pass

    @classmethod
    def get_config(cls):
        """get_config 获取信息

        :return: 返回包含信息的字典
        :rtype: dict
        """

        ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config', 'config.ini')
        # ini_path = r'I:\my_python_spider\spider_on_3dm\config\config.ini'
        config = ConfigParser()
        config.read(ini_path, encoding='utf-8')

        d_config = {}
        for config in config.items('configuration'):
            # TODO: 需要确认是否对true值进行转换
            # 暂时不对true进行转换,均按照str处理
            # d[config[0]] = True if lower(config[1]) == 'true' else config[1]
            d_config[config[0]] = config[1]

        d_config['now_date'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
        return d_config


if __name__ == '__main__':
    TMP_D = GetConfig.get_config()
    print(TMP_D)
