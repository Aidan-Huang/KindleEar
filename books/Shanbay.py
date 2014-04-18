#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import urlparse
import copy
import tempfile
import os
import time
from base import BaseFeedBook
from ShanbaySearcher import ShanbaySearcher


def getBook():
    return Shanbay

class Shanbay(BaseFeedBook):

    title                 = u'ShanBay'
    description           = u'ShanBay'
    language              = 'en' 
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_default.gif"
    coverfile             = "" #封面图片文件
    network_timeout       = 60
    oldest_article        = 1
    #设置为True排版也很好（往往能更好的剔除不相关内容），
    #除了缺少标题下的第一幅图
    fulltext_by_readability = True
    
    
    # feeds = [
    #         (u'ShanbayNews', 'http://www.shanbay.com/read/news/'),
    #        ]

    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """

        return ShanbaySearcher().search()


# class main(object):

#     shanbay = Shanbay()

#     # shanbay.ParseFeedUrls()



# if __name__ == '__main__':
#      main()