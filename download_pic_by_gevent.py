#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__time__ = 2018/11/11 13:41
__author__ = Kexin Xu
__desc__ = 输入title中的网址,对网址内容进行解析获取每一页上的图片下载地址
           使用协程
"""

# 将IO转为异步执行的函数
from gevent import monkey
monkey.patch_all()

import time
import gevent
from gevent.queue import Queue #, Empty

from get_title_urls import GetTitleUrls



class DownloadByGevent(GetTitleUrls):

    def __init__(self, download_urls):
        super(DownloadByGevent, self).__init__()
        self.workQueue = Queue(1000)
        self.download_urls = download_urls

    def crawler(self, index):
        Process_id = 'Process-' + str(index)
        while not self.workQueue.empty():
            url = self.workQueue.get(timeout=2)
            try:
                r = self.get_soup(url, timeout=20)
                my_write(str(' '.join([str(x) for x in [Process_id, self.workQueue.qsize(), r.status_code, url]])))
            except Exception as e:
                # print(Process_id, self.workQueue.qsize, url, 'Error: ', e)
                my_write(str(' '.join([str(x) for x in [Process_id, self.workQueue.qsize(), r.status_code, url]])))
    
    def boss(self):
        for url in self.download_urls:
            self.workQueue.put_nowait(url)

    def start(self):
        start_time = time.time()
        gevent.spawn(self.boss).join()
        jobs = []
        for i in range(10):
            jobs.append(gevent.spawn(self.crawler, i))

        gevent.joinall(jobs)
        print('end')
        print("爬虫时间为%s"%time.time() - start_time)
    

if __name__ == '__main__':
    res = ['https://www.3dmgame.com/bagua/525.html', 'https://www.3dmgame.com/bagua/514.html', 'https://www.3dmgame.com/bagua/511.html', 'https://www.3dmgame.com/bagua/508.html', 'https://www.3dmgame.com/bagua/507.html', 'https://www.3dmgame.com/bagua/504.html', 'https://www.3dmgame.com/bagua/502.html', 'https://www.3dmgame.com/bagua/501.html', 'https://www.3dmgame.com/bagua/493.html', 'https://www.3dmgame.com/bagua/491.html', 'https://www.3dmgame.com/bagua/486.html', 'https://www.3dmgame.com/bagua/485.html', 'https://www.3dmgame.com/bagua/484.html', 'https://www.3dmgame.com/bagua/483.html', 'https://www.3dmgame.com/bagua/481.html', 'https://www.3dmgame.com/bagua/480.html', 'https://www.3dmgame.com/bagua/479.html', 'https://www.3dmgame.com/bagua/473.html', 'https://www.3dmgame.com/bagua/472.html', 'https://www.3dmgame.com/bagua/470.html', 'https://www.3dmgame.com/bagua/467.html', 'https://www.3dmgame.com/bagua/465.html', 'https://www.3dmgame.com/bagua/459.html', 'https://www.3dmgame.com/bagua/456.html', 'https://www.3dmgame.com/bagua/455.html', 'https://www.3dmgame.com/bagua/452.html', 'https://www.3dmgame.com/bagua/446.html', 'https://www.3dmgame.com/bagua/444.html', 'https://www.3dmgame.com/bagua/442.html', 'https://www.3dmgame.com/bagua/436.html', 'https://www.3dmgame.com/bagua/431.html', 'https://www.3dmgame.com/bagua/429.html', 'https://www.3dmgame.com/bagua/428.html', 'https://www.3dmgame.com/bagua/427.html', 'https://www.3dmgame.com/bagua/421.html', 'https://www.3dmgame.com/bagua/416.html', 'https://www.3dmgame.com/bagua/415.html', 'https://www.3dmgame.com/bagua/413.html', 'https://www.3dmgame.com/bagua/409.html', 'https://www.3dmgame.com/bagua/402.html', 'https://www.3dmgame.com/bagua/396.html', 'https://www.3dmgame.com/bagua/384.html', 'https://www.3dmgame.com/bagua/381.html', 'https://www.3dmgame.com/bagua/377.html', 'https://www.3dmgame.com/bagua/376.html', 'https://www.3dmgame.com/bagua/375.html', 'https://www.3dmgame.com/bagua/365.html', 'https://www.3dmgame.com/bagua/361.html', 'https://www.3dmgame.com/bagua/355.html', 'https://www.3dmgame.com/bagua/354.html', 'https://www.3dmgame.com/bagua/353.html', 'https://www.3dmgame.com/bagua/352.html', 'https://www.3dmgame.com/bagua/343.html', 'https://www.3dmgame.com/bagua/338.html', 'https://www.3dmgame.com/bagua/335.html', 'https://www.3dmgame.com/bagua/332.html', 'https://www.3dmgame.com/bagua/329.html', 'https://www.3dmgame.com/bagua/328.html', 'https://www.3dmgame.com/bagua/323.html', 'https://www.3dmgame.com/bagua/322.html', 'https://www.3dmgame.com/bagua/319.html', 'https://www.3dmgame.com/bagua/317.html', 'https://www.3dmgame.com/bagua/314.html', 'https://www.3dmgame.com/bagua/307.html', 'https://www.3dmgame.com/bagua/302.html', 'https://www.3dmgame.com/bagua/300.html', 'https://www.3dmgame.com/bagua/299.html', 'https://www.3dmgame.com/bagua/298.html', 'https://www.3dmgame.com/bagua/278.html', 'https://www.3dmgame.com/bagua/273.html', 'https://www.3dmgame.com/bagua/247.html', 'https://www.3dmgame.com/bagua/245.html', 'https://www.3dmgame.com/bagua/241.html', 'https://www.3dmgame.com/bagua/235.html', 'https://www.3dmgame.com/bagua/231.html', 'https://www.3dmgame.com/bagua/229.html', 'https://www.3dmgame.com/bagua/226.html', 'https://www.3dmgame.com/bagua/210.html', 'https://www.3dmgame.com/bagua/209.html', 'https://www.3dmgame.com/bagua/206.html', 'https://www.3dmgame.com/bagua/203.html', 'https://www.3dmgame.com/bagua/195.html', 'https://www.3dmgame.com/bagua/193.html', 'https://www.3dmgame.com/bagua/190.html', 'https://www.3dmgame.com/bagua/180.html', 'https://www.3dmgame.com/bagua/179.html', 'https://www.3dmgame.com/bagua/178.html', 'https://www.3dmgame.com/bagua/162.html', 'https://www.3dmgame.com/bagua/157.html', 'https://www.3dmgame.com/bagua/152.html', 'https://www.3dmgame.com/bagua/144.html', 'https://www.3dmgame.com/bagua/136.html', 'https://www.3dmgame.com/bagua/128.html', 'https://www.3dmgame.com/bagua/125.html', 'https://www.3dmgame.com/bagua/121.html', 'https://www.3dmgame.com/bagua/118.html', 'https://www.3dmgame.com/bagua/103.html', 'https://www.3dmgame.com/bagua/95.html', 'https://www.3dmgame.com/bagua/82.html', 'https://www.3dmgame.com/bagua/73.html', 'https://www.3dmgame.com/bagua/70.html', 'https://www.3dmgame.com/bagua/61.html', 'https://www.3dmgame.com/bagua/58.html', 'https://www.3dmgame.com/bagua/57.html', 'https://www.3dmgame.com/bagua/27.html', 'https://www.3dmgame.com/bagua/26.html', 'https://www.3dmgame.com/bagua/19.html', 'https://www.3dmgame.com/bagua/14.html', 'https://www.3dmgame.com/bagua/11.html', 'https://www.3dmgame.com/bagua/8.html']
    DownloadByGevent(res).start()


    




    

