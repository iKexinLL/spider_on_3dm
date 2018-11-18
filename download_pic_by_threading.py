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
from get_config import GetConfig

NOW_DATE = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
NOW_TIME = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')
IF_TEST_PROGRAMM = GetConfig.get_config()['if_test_programm']
assert IF_TEST_PROGRAMM in ('true', 'false'), '请在config.ini中填写 true 或 false'

class DownloadPicByThreading(threading.Thread):
    """多线程下载
    
    Parameters
    ----------
    threading : thread
        python多线程的包
    
    """

    def __init__(self, que_, log_path, f_write_urls):
        threading.Thread.__init__(self)

        self.sleep_program = RandomSleepTime()
        self.que = que_
        self.downloaded_urls_path = PicFileHandle.get_downloaded_urls_path()
        self.log_path = log_path
        self.f_write_urls = f_write_urls
        # 异常处理
        self.exc = None

    def run(self):
        while True:
            self.sleep_program.sleep(0)
            url, mid_pic_name, mid_pic_folder_path = self.que.get()
            
            start_time = datetime.datetime.now()
            r = requests.get(url)
            img_contents = r.content
            content_type = r.headers['Content-Type']

            mid_pic_folder_path = PicFileHandle.replace_invalid_char(mid_pic_folder_path)
            
            mid_pic_name = PicFileHandle.replace_invalid_char(mid_pic_name)
            mid_pic_name = mid_pic_name + '.' + content_type.split('/')[1]

            pic_file_path = os.path.join(mid_pic_folder_path, mid_pic_name)

            # 添加子线程的异常处理
            try:
                with open(pic_file_path, 'wb') as f_pics:
                    f_pics.write(img_contents)
                    self.f_write_urls.write(url + '\n')
                    runing_time = datetime.datetime.now() - start_time
                    runing_time = str(runing_time.seconds) + '.' + str(runing_time.microseconds)[:2]  
                    self.pic_log(runing_time, os.path.split(pic_file_path)[1], url)

            except IOError as io_e:
                import sys
                print('Exception e is ' + str(io_e))
                self.exc = sys.exc_info()

            finally:
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

    title_urls = GetTitleUrls().return_title_urls(if_test_programm=IF_TEST_PROGRAMM)
    mid_log_path = PicFileHandle.get_logger_file_path()

    # 获取downloaded_urls文件的路径
    downloaded_urls_path = PicFileHandle.get_downloaded_urls_path()
    # 获取downloaded_urls内容
    downloaded_urls = PicFileHandle.get_downloaded_urls()
            
    for title_url in title_urls:
        pic_info = GetPicInfoInTitlePages().return_pic_info(title_url, 
                                                            if_test_programm=IF_TEST_PROGRAMM)

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
                # mid_pic_file_path = PicFileHandle.get_pic_file_path(
                #     k, pic_info[k], pic_folder_path)
                que.put((k, pic_info[k], pic_folder_path))

                if IF_TEST_PROGRAMM == 'true':
                    break
    
    # 关于这个循环放在for k in pic_info外面的解释
    # 当这个循环在里面时,每个循环,都会创建五个线程,造成线程超多
    # 20181115_171927 我不确定为什么下载完的线程为什么没结束
    with open(downloaded_urls_path, 'a', encoding='utf-8') as f:
        for _ in range(5):
            t = DownloadPicByThreading(que, mid_log_path, f)
            t.setDaemon(True)
            t.start()

        que.join()
    
    print('Program End')



# 为什么不使用 t = DownloadPicByThreading(que, pic_info) 中pic_info(dict)?
# 因为在多线程中,线程A中可能是已经传入了新的页面的网址,线程B仍就使用pic_info,导致数据差异
# 产生keyError,所以将其拆分,直接传入数据


# pic_info = {'pic_explain': '9月17日是日本的《敬老节》，近日人气急升的漫画《黄金神威》则适时推出敬老版《白银神威》，
# 原作中诸位豪杰全部化为白发老人，读起来别有一番滋味。', 
# 'pic_title': '日式搞笑来袭！人气漫画《黄金神威》推敬老白银神威', 
# 'https://img.3dmgame.com/uploads/images/news/20180918/1537262474_106428.png': 
# '0101_·一起来欣赏下对比后的画面，怎样，突然老化后的众位角色是不是另有一番新感觉？感兴趣的小伙伴可以去特设网站阅读。
# https://youngjump.jp/goldenkamuy/contents/silverkamuy/', 
# 'https://img.3dmgame.com/uploads/images/news/20180918/1537262486_229261.png': 
# '0102_None_20181118_180307_1', 
# 'https://img.3dmgame.com/uploads/images/news/20180918/1537262486_888511.png': 
# '0103_None_20181118_180307_2', 
# 'https://img.3dmgame.com/uploads/images/news/20180918/1537262486_163710.png': 
# '0104_None_20181118_180307_3', 
# 'https://img.3dmgame.com/uploads/images/news/20180918/1537262486_732005.png': 
# '0105_None_20181118_180307_4'}
