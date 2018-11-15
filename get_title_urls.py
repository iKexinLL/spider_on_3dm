#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/08 18:31
__author__ = Kexin Xu
__desc__ = 获取页面 https://www.3dmgame.com/bagua_65_6/ 上的标题地址
           不太确定这个地址是否会变(因为这个网址有些不符合规范...)
"""

import requests
from bs4 import BeautifulSoup


from get_config import GetConfig
from random_sleep_time import RandomSleepTime
from logging_info import LogginInfoOnlyStream


class GetTitleUrls():
    """GetTitleUrls 获取根目录下的标题网址
    """

    def __init__(self):
        # self.config = GetConfig.get_config()['root_url'] 
        # self._max_download_pages = config['max_download_pages']
        # self.config = GetConfig.get_config()
        self.sleep_program = RandomSleepTime()
        
    def get_soup(self, url, timeout=10):
        """将网站内容转换成BeautifulSoup对象

        Returns
        -------
        bs4.BeautifulSoup
            BeautifulSoup对象
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                                 'AppleWebKit/537.36 (KHTML, like Gecko) ' + 
                                 'Chrome/70.0.3538.77 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=timeout)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')

        return soup

    def get_title_urls(self, soup):
        """根据soup,找出所需的网址
        
        Parameters
        ----------
        soup : bs4.BeautifulSoup
            BeautifulSoup对象
        
        Returns
        -------
        list
            title网址合集
        """

        tp_all_title_info = soup.find_all(class_='selectarcpost')
        all_title_urls = []

        for i in tp_all_title_info:
            all_title_urls.append(i['href'])

        return all_title_urls

    def get_next_page(self, soup):
        """获取下一页面的网址
        
        Parameters
        ----------
        soup : bs4.BeautifulSoup
            BeautifulSoup对象
        
        Returns
        -------
        str
            下一页的网址
        """

        next_button = soup.find(class_='next')

        # 若存在下一页,则返回下一页的网址
        # 增加判断,防止next_button未None时报错
        if next_button:
            if next_button.a:
                return next_button.a['href']

    def return_title_urls(self, if_break=False):
        """调用其它方法,返回所有的title网址
        
        Parameters
        ----------
        if_break : bool, optional
            减少循环,方便对程序进行测试 (the default is False, which 不循环)
        
        Returns
        -------
        list
            返回所有的title网址
        """
        url = GetConfig.get_config()['root_url']
        log = LogginInfoOnlyStream()
        temp_res = []
        while url:
            log.info("getting title url in : " + url)
            soup = self.get_soup(url)
            self.sleep_program.sleep(0)
            temp_res.extend(self.get_title_urls(soup))
            url = self.get_next_page(soup)
            if if_break:
                break

        return temp_res
                

if __name__ == '__main__':
    tp = GetTitleUrls()
    res = tp.return_title_urls()
    print(res)
