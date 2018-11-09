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



class GetTitleUrls():
    """GetTitleUrls 获取根目录下的标题网址
    """
    def __init__(self):
        # self.config = GetConfig.get_config()['root_url'] 
         # self._max_download_pages = config['max_download_pages']
        self._config = GetConfig.get_config()
        

    def __get_soup(self, url):
        """将网站内容转换成BeautifulSoup对象
        
        Returns
        -------
        bs4.BeautifulSoup
            BeautifulSoup对象
        """

        # r = requests.get(self._config['root_url'])
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')

        return soup

    def __get_title_urls(self, soup):
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

    def __get_next_page(self, soup):
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

        if next_button.a:
            # 若存在下一页,则返回下一页的网址
            return next_button.a['href']

    def start(self):
        """调用其它方法,返回所有的title网址
        
        Returns
        -------
        list
            返回所有的title网址
        """

        url = self._config['root_url']
        res = []
        while url:
            soup = self.__get_soup(url)
            res.extend(self.__get_title_urls(soup))
            url = self.__get_next_page(soup)

        return res
                

if __name__ == '__main__':
    tp = GetTitleUrls()
    res = tp.start()
