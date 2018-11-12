#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/11 13:45
__author__ = Kexin Xu
__desc__ = 输入title中的网址,对网址内容进行解析获取每一页上的图片下载地址
"""

import time
from bs4 import Tag

from get_title_urls import GetTitleUrls

class GetPicUrlInPages(GetTitleUrls):
    """输入title中的网址,对网址内容进行解析获取每一页上的图片下载地址
    
    """

    def __init__(self):
        """初始化父类__init__方法
        
        """
        super(GetPicUrlInPages, self).__init__()
        # self.get_pic_url_and_info(soup)

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
            mid_res_d['pic_title'] = ''.join(soup.find('h1',class_='bt').text.split())
        
        # 获取所有图片网址的元素
        # [<img alt="..." src="..."/>]
        all_img_eles = soup.find_all(self.img_has_alt)

        for n, img_ele in enumerate(all_img_eles):
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

            mid_res_d[img_ele['src']] = img_explain

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

    def start(self, url=r'https://www.3dmgame.com/bagua/540.html'):
        """仅作测试使用
        
        Returns
        -------
        dict
            pic_explain -> title说明
            图片网址 -> 图片说明
        """
        # url = r'https://www.3dmgame.com/bagua/525.html'
        res_d = {}

        while url:
            print('url in get_pic_url_in_pages is ' + url)
            soup = self.get_soup(url)
            res_d.update(self.get_pic_url_and_info(soup))
            self.sleep_program.sleep(3)
            url = self.get_next_page(soup)
            
        return res_d


if __name__ == '__main__':
    tp = GetPicUrlInPages().start()
    print(tp)
    # {'https://img.3dmgame.com/uploads/images/news/20181107/1541583036_205040.jpg': 'None_20181112_150124_0', 
    # 'https://img.3dmgame.com/uploads/images/news/20181107/1541583036_947114.jpg': 'None_20181112_150124_1', 
    # 'https://img.3dmgame.com/uploads/images/news/20181107/1541583036_163179.jpg': 'None_20181112_150124_2', 
    # 'https://img.3dmgame.com/uploads/images/news/20181107/1541583037_237890.jpg': 'None_20181112_150124_3', 
    # 'https://img.3dmgame.com/uploads/images/news/20181107/1541583038_155306.jpg': 'None_20181112_150124_4'}
    # 'pic_explain': '转眼又到周四了，快来看看新的福利囧图吧！朦朦胧胧的小姐姐就是美，让人心中渴望。
    # 现在的女装大佬是越来越多了，已经雌雄难辨。劈叉还不忘挑逗
    # 妹子，你们太过分了。美女老师穿得如此性感诱惑，学生们还有心思上课吗？'