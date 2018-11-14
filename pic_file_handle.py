#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/12 15:03
__author__ = Kexin Xu
__desc__ = 处理pic相关的路径以及文件夹,文件操作
           包括创建,清空,删除文件(夹)
"""

import os
import re
import datetime

from get_config import GetConfig

NOW_DATE = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
NOW_TIME = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')

class PicFileHandle():
    """处理此程序中关于路径的类
    
    Returns
    -------
    None
        处理此程序中关于路径的类
    """

    __root_folder_path = GetConfig.get_config()['root_folder_path']

    def __init__(self):
        pass
    
    @staticmethod
    def replace_invalid_char(path):
        r"""剔除windows路径或文件上的非法字符
           规则: r'\*|\?|"|<|>|\||\u3000'
        
        Parameters
        ----------
        path : str
            文件或文件夹路径
        
        Returns
        -------
        str
            剔除后的路径
        """

        re_compile = re.compile(r'\*|\?|"|<|>|\||\u3000')
        return re.sub(re_compile, '_', path)

    @staticmethod
    def create_folder(path):
        """根据path创建文件夹
        
        Parameters
        ----------
        path : str
            文件夹路径
        
        """
        if not os.path.exists(PicFileHandle().replace_invalid_char(path)):
            os.makedirs(path)

    @staticmethod
    def remove_file(path):
        """删除文件,防止文件重复
        
        Parameters
        ----------
        path : str
            文件路径
        
        """

        if os.path.isfile(PicFileHandle().replace_invalid_char(path)):
            os.remove(path)

    @staticmethod
    def path_join(path, *paths):
        """同os.path.join,合并N个路径
        
        Parameters
        ----------
        path : str
            路径
        
        Returns
        -------
        str
            合并后的路径
        """

        fisrt_path = PicFileHandle.replace_invalid_char(path)
        other_paths = []
        for tmp_path in paths:
            other_paths.append(PicFileHandle.replace_invalid_char(tmp_path))
        return os.path.join(fisrt_path, *other_paths)

    @staticmethod
    def isfile(path):
        """判断path路径是否为文件
        
        Parameters
        ----------
        path : str
            文件路径
        
        Returns
        -------
        bool
            true -> 是
            flase -> 不是
        """

        return os.path.isfile(path)

    @staticmethod
    def get_root_folder_path():
        """返回config中配置的根目录
        
        Returns
        -------
        str
            根目录路径
        """

        # return GetConfig.get_config()['root_folder_path']
        return PicFileHandle.__root_folder_path

    @staticmethod
    def get_pic_folder_path(pic_title):
        """返回存储pic的文件夹路径
        
        Parameters
        ----------
        pic_title : str
            使用pic_title作为文件夹名称
        
        Returns
        -------
        str
            存储pic的文件夹路径
        """

        # root_folder_path = PicFileHandle.get_root_folder_path()
        pic_folder_path = PicFileHandle.path_join(
            PicFileHandle.__root_folder_path, NOW_DATE, pic_title)

        return pic_folder_path

    @staticmethod
    def get_pic_file_path(url, prefix_name, pic_folder_path):
        """返回存储pic的路径
        
        Parameters
        ----------
        url : str
            pic网址,用于获取文件类型
        prefix_name : str
            文件名称,一般为图片下方的说明
        pic_folder_path : str
            存储pic的文件夹路径
        
        Returns
        -------
        str
            返回存储pic的路径
        """

        suffix_name = '.' + url.rsplit('.', 1)[1]
        pic_name = prefix_name + suffix_name
        return PicFileHandle.path_join(pic_folder_path, pic_name)

    @staticmethod
    def get_logger_file_path():
        """返回log的路径
        
        Returns
        -------
        str
            log的路径
        """

        # root_folder_path = PicFileHandle.get_root_folder_path()
        pic_logger_path = PicFileHandle.path_join(
            PicFileHandle.__root_folder_path, NOW_DATE, 'LOG', 'pic_log_%s.log'%NOW_TIME)
        PicFileHandle.create_folder(os.path.split(pic_logger_path)[0])
        return pic_logger_path

    @staticmethod
    def get_downloaded_urls_path():
        """返回downloaded_urls的路径
        
        Returns
        -------
        str
            downloaded_urls的路径
        """

        return PicFileHandle.path_join(
            PicFileHandle.__root_folder_path, 'downloaded_urls.txt')
        
    @staticmethod
    def get_downloaded_urls():
        """获取已下载的pic地址
        
        Returns
        -------
        set
            已下载的pic地址
        """

        st = set()
        mid_path = PicFileHandle.get_downloaded_urls_path()
        PicFileHandle.clear_downloaded_urls()

        with open(mid_path) as f:
            for i in f.readlines():
                st.add(''.join(i.split()))
            return st

    @staticmethod
    def clear_downloaded_urls():
        """重置(清空)downloaded_urls.txt
        
        """

        mid_path = PicFileHandle.get_downloaded_urls_path()
        if not PicFileHandle.isfile(mid_path):
            with open(mid_path, 'w'):
                pass

    @staticmethod
    def write_pic_explain(title_url, pic_explain, pic_folder_path):
        """将pic_explain的内容写入到pic根目录
        
        Parameters
        ----------
        title_url : str
            爬取的pic网址,方便之后查找
        pic_explain : str
            title说明
        pic_folder_path : str
            pic的根目录
        
        """
        mid_path = PicFileHandle.path_join(pic_folder_path, 'pic_explain.txt')
        with open(mid_path, 'w', encoding='utf-8') as f:
            f.write(title_url + '\n')
            f.write(pic_explain)

if __name__ == '__main__':
    print(PicFileHandle.write_pic_explain('w', 'qwe', r'e:\temp'))





    
