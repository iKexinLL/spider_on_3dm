#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/11 23:31
__author__ = Kexin Xu
__desc__ = 返回一个睡眠时间,方式爬虫被封锁
"""

import random
import time

# from logging_info import LogginInfoOnlyStream

class RandomSleepTime():
    """返回一个睡眠时间,方式爬虫被封锁
    
    """


    def __init__(self):
        self.scrap_times = 0

    def random_time(self, base_time):
        """生成一个(base_time,base_time+1)或(0,3)之间的随机数
        大小取决于调用的次数
        
        Parameters
        ----------
        base_time : int, optional
            睡眠的时间基数 (the default is 5)
        
        Returns
        -------
        float
            睡眠的时间
        """

        self.scrap_times += 1
        if self.scrap_times % 5 == 0:
            sleep_time = base_time + random.random()
        else:
            sleep_time = random.randint(0, 1) + random.random()
        
        return sleep_time

    def sleep(self, base_time=5):
        """根据random_time()产生的时间,暂停程序
        
        """
        base_time = 0 if base_time == 0 else base_time
        sleep_time = self.random_time(base_time)
        # print('睡眠: %s秒'%sleep_time)
        # LogginInfoOnlyStream().info('睡眠: %s秒'%sleep_time)
        time.sleep(sleep_time)
