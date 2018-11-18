#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/11 13:45
__author__ = Kexin Xu
__desc__ = 输入title中的网址,对网址内容进行解析获取每一页上的图片下载地址
"""

import time
from bs4 import Tag
# from collections import namedtuple

from get_title_urls import GetTitleUrls
from logging_info import LogginInfoOnlyStream

class GetPicInfoInTitlePages(GetTitleUrls):
    """输入title中的网址,对网址内容进行解析获取每一页上的图片下载地址
    
    """

    def __init__(self):
        """初始化父类__init__方法
        
        """
        super(GetPicInfoInTitlePages, self).__init__()
        # self.pic_info = namedtuple('picInfo', ['pic_name', 'pic_location'])
        self.h = lambda num: str(num) if int(num) > 9 else '0' + str(num) 
        # self.get_pic_url_and_info(soup)

    def get_format_num(self, *num):
        """返回格式化的两位数字 1 -> 01, 13 -> 13
        
        Parameters
        ----------
        num : str or num
            需要格式化的数字(或能转换成数字的字符串)
        
        Returns
        -------
        str
            返回格式化的两位数字 1 -> 01, 13 -> 13
        """

        return ''.join([self.h(x) for x in num])

    def get_pic_url_and_info(self, soup):
        """获取图片,以及图片下方的说明作为图片名称
        
        Parameters
        ----------
        soup : bs4.BeautifulSoup
            BeautifulSoup对象
        
        Returns
        -------
        dict
            pic_explain -> title说明
            图片网址 -> 图片说明
        """

        mid_res_d = {}
        
        # 获取当前soup的页码
        # 添加判断class_='active',对只有一页的网页进行判断
        if soup.find(class_='active'):
            page_num = soup.find(class_='active').text
        else:
            page_num = '1'

        # 获取第一页的整体说明 -> 第一页的第一个P元素
        if page_num == '1':
            mid_res_d['pic_explain'] = ''.join(soup.find('p').text.split()) # 去除\r\n\t等占位符
            mid_res_d['pic_title'] = ''.join(soup.find('h1', class_='bt').text.split())
        
        # 获取所有图片网址的元素
        # [<img alt="..." src="..."/>]
        all_img_eles = soup.find_all(self.img_has_alt)

        for n, img_ele in enumerate(all_img_eles):

            pic_location = self.get_format_num(page_num, (n+1))
            # 获取img的父元素的兄弟元素(叔叔吗?)
            # 判断其是否为Tag元素,并尝试获取其内容作为名称
            # 如无Tag元素,则将其视为无说明,将None+时间+顺序作为名称
            # 无Tag元素的例子https://www.3dmgame.com/bagua/525_48.html
            for mid_img_explain in img_ele.parent.next_siblings:
                if isinstance(mid_img_explain, Tag) and mid_img_explain.span:
                    img_explain = ''.join(mid_img_explain.text.split())
                    break
            else:
                img_explain = "None_" + time.strftime('%Y%m%d_%H%M%S') + '_' + str(n)

            mid_res_d[img_ele['src']] = pic_location + '_' + img_explain
                # self.pic_info(img_explain, self.get_format_num(page_num, n))

        return mid_res_d

    def img_has_alt(self, tag):
        """查找带有alt属性的img
        
        Parameters
        ----------
        tag : soup.find_all 自动传入
            元素名称
        
        Returns
        -------
        bool
            返回bool作为判断依据
        """

        return tag.has_attr('alt')

    def url_log(self, url):
        """在控制台输出url
        
        Parameters
        ----------
        url : str
            pic网址
        
        """

        log = LogginInfoOnlyStream()
        log.info('getting pic url from title: ' + url)

    def return_pic_info(self, url=r'https://www.3dmgame.com/bagua/540.html', 
                        if_test_programm='false'):
        """返回pic的信息,网址以及名称
        
        Parameters
        ----------
        url : regexp, optional
            title网址 (the default is r'https://www.3dmgame.com/bagua/540.html', which 默认测试的title网址)
        if_test_programm : str, optional
            注意,这里只可填写 true 和 false
            减少循环,方便对程序进行测试 (the default is False, which 不循环)
        Returns
        -------
        dict
            pic_explain -> title说明
            图片网址 -> 图片说明
        """
        # url = r'https://www.3dmgame.com/bagua/525.html'
        res_d = {}

        while url:
            #print('url in get_pic_url_in_title_pages is ' + url)
            soup = self.get_soup(url)
            self.url_log(url)
            res_d.update(self.get_pic_url_and_info(soup))
            self.sleep_program.sleep(1)
            url = self.get_next_page(soup)
            if if_test_programm == 'true':
                break
            
        return res_d


if __name__ == '__main__':
    tp = GetPicInfoInTitlePages().return_pic_info(if_test_programm='true')
    print(tp)
    # tp = {'pic_explain': '周一来临，快来欣赏云飞系列的新内涵囧图。美女姿势诱惑，你们有大胆的想法吗？\
    # 救人一命胜造七级浮屠，妹子这么痛苦就让我来帮忙吧！小姐姐胸前的字太霸气，是男人都蠢蠢欲动。大叔看到什么吓成这样，难道是被性感美女吓坏了？', 
    # 'pic_title': '周一内涵囧图云飞系列美女姿势诱惑你们有大胆想法吗？', 
    # 'http://wx1.sinaimg.cn/mw690/4496435egy1fx3rzkz4v1g209n0l5e85.gif': '0101_韩国BJ', 
    # 'http://wx4.sinaimg.cn/mw690/006khmFply1fx0s05q4cig308c04t1kx.gif': '0102_野外捡到屠龙刀', 
    # 'http://wx4.sinaimg.cn/mw690/006khmFply1fx0s2u59dag304t078x6p.gif': '0103_终于看见一只不怕猫的狗', 
    # 'https://img.3dmgame.com/uploads/images/news/20181111/1541893418_188055.jpg': '0104_程序员的不甘'}
    