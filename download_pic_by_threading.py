#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/12 14:52
__author__ = Kexin Xu
__desc__ = 通过threading方式进行多进程下载,这个比较熟悉
"""

import threading
import datetime
import queue
import os
import requests


from pic_file_handle import PicFileHandle
from random_sleep_time import RandomSleepTime
from get_title_urls import GetTitleUrls
from get_pic_info_in_title_pages import GetPicInfoInTitlePages
from logging_info import LogginInfo

NOW_DATE = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
NOW_TIME = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')

class DownloadPicByThreading(threading.Thread):
    """多线程下载
    
    Parameters
    ----------
    threading : thread
        python多线程的包
    
    """

    def __init__(self, que_, log_path, f_urls):
        threading.Thread.__init__(self)

        self.sleep_program = RandomSleepTime()
        self.que = que_
        self.downloaded_urls_path = PicFileHandle.get_downloaded_urls_path()
        self.log_path = log_path
        self.f_urls = f_urls

    def run(self):
        while True:
            self.sleep_program.sleep(0)
            url, pic_file_path = self.que.get()

            start_time = datetime.datetime.now()          
            img_contents = requests.get(url).content
            with open(pic_file_path, 'wb') as f_pics:
                f_pics.write(img_contents)
                f_urls.write(url + '\n')
                runing_time = datetime.datetime.now() - start_time
                runing_time = str(runing_time.seconds) + '.' + str(runing_time.microseconds)[:2]  
                self.pic_log(runing_time, os.path.split(pic_file_path)[1], url)
            
            self.que.task_done()

    def pic_log(self, download_time, pic_name, url):
        """插入日志
        
        Parameters
        ----------
        download_time : str
            下载时间
        url : str
            pic网址
        pic_name : str
            pic名称
        
        """

        log = LogginInfo(logFilename=self.log_path)
        log.debug(download_time + 's ' + pic_name + ' ' + url)
        

if __name__ == '__main__':

    # 1.获取所有的title
    # 2.解析title,获取title标题(pic_title),title中的说明(pic_explain),title中所有pic网址
    # 3.根据pic_title创建存储的文件夹

    que = queue.Queue()

    title_urls = GetTitleUrls().return_title_urls(if_break=False)
    mid_log_path = PicFileHandle.get_logger_file_path()

    # 获取downloaded_urls文件的路径
    downloaded_urls_path = PicFileHandle.get_downloaded_urls_path()
    # 获取downloaded_urls内容
    downloaded_urls = PicFileHandle.get_downloaded_urls()

    for title_url in title_urls:
        pic_info = GetPicInfoInTitlePages().return_pic_info(title_url, if_break=False)

        pic_explain = pic_info.get('pic_explain', 'None_Pic_Explain_' + NOW_TIME)
        pic_title = pic_info.get('pic_title', 'None_Pic_Title_' + NOW_TIME)

        # 获取存储pic的文件夹路径
        pic_folder_path = PicFileHandle.get_pic_folder_path(pic_title)
        # 创建存储pic的文件夹
        PicFileHandle.create_folder(pic_folder_path)
        # 将pic_explain写入到pic文件夹内
        PicFileHandle.write_pic_explain(title_url, pic_explain, pic_folder_path)

        for k in pic_info:
            if k not in ('pic_explain', 'pic_title') and k not in downloaded_urls:
                mid_pic_file_path = PicFileHandle.get_pic_file_path(
                    k, pic_info[k], pic_folder_path)
                que.put((k, mid_pic_file_path))
        
        break
    
    # 关于这个循环放在for k in pic_info外面的解释
    # 当这个循环在里面时,每个循环,都会创建五个线程,造成线程超多
    # 20181115_171927 我不确定为什么下载完的线程为什么没结束
    with open(downloaded_urls_path, 'a', encoding='utf-8') as f_urls:
        for _ in range(5):
            t = DownloadPicByThreading(que, mid_log_path, f_urls)
            t.setDaemon(True)
            t.start()

        que.join()
    
    print('program end')



# 为什么不使用 t = DownloadPicByThreading(que, pic_info) 中pic_info(dict)?
# 因为在多线程中,线程A中可能是已经传入了新的页面的网址,线程B仍就使用pic_info,导致数据差异
# 产生keyError,所以将其拆分,直接传入数据
