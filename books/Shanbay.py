#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

from bs4 import BeautifulSoup

import urlparse
import copy
import urllib2 
import tempfile
import os
import time

class ShanbayNews(object):
    """An article of news in Shanbay"""
    def __init__(self, title, source, date):
        self.title = title
        self.source = source
        self.date = date

        if 'feeds.reuters.com' == source:
            self.search = ReutersSearcher()
        elif 'voanews.com' == source:
            self.search = VOASearcher()
        

    def get_url(self):
        
        return self.search.get_url(self.title)


class SearchException(Exception):
    """fitting article exception"""
    pass

class URLSearcher(object):

    def get_url(self, title):
        pass

class VOASearcher(URLSearcher):

    
    site = 'http://www.voanews.com'
    search_url = '/search/?k='


    #Deadly Virus Surges Through Arab Gulf



    def get_url(self, title):

        self.title = "\"" + title.replace(' ', '%20') + "\""


        d = urllib2.urlopen(self.site + self.search_url + self.title)

        soup = BeautifulSoup(d.read().decode('utf-8'))

        url = soup.find('a', attrs = {'class': 'linkmed'})['href']
            

        return self.site + url

class ReutersSearcher(URLSearcher):


    site = 'http://www.reuters.com'
    search_url = '/search?blob='

    #Apple+antitrust+compliance+off+to+a+promising+start%3A+monitor


    #Apple antitrust compliance off to a promising start: monitor

    def get_url(self, title):

        self.title = title.replace(' ', '+').replace(':', '%3A')

        d = urllib2.urlopen(self.site + self.search_url + self.title)

        soup = BeautifulSoup(d.read().decode('utf-8'))

        url = soup.find('li', attrs = {'class': 'searchHeadline'}).a
            

        return url['href']
 


def getBook():
    return Shanbay


# from base import BaseFeedBook
# class Shanbay(BaseFeedBook):
class Shanbay(object):
    title                 = u'ShanBay'
    description           = u'ShanBay'
    language              = 'en' 
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    network_timeout       = 60
    oldest_article        = 1
    #设置为True排版也很好（往往能更好的剔除不相关内容），
    #除了缺少标题下的第一幅图
    fulltext_by_readability = True
    
    
    feeds = [
            (u'ShanBayNews', 'http://www.shanbay.com/read/news/'),
           ]

    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        urls = []
        feedtitle = 'ShanbayNews'
        url = 'http://www.Shanbay.com/read/news/'

        d = urllib2.urlopen(url)

        soup = BeautifulSoup(d.read().decode('utf-8'))
    

        urls = []

        for article in soup.find_all('div', attrs = {'class': 'article'}):
            title = article.find('div', attrs = {'class': 'title'}).a.string
            info = article.find('div', attrs = {'class': 'info'}).find_all('span')


            source = info[0].string
            date = info[1].string
            
    
            #print 'title:' + title + ' | source:' + source + ' | date:' + date
    
            article = ShanbayNews(title, source, date)
    
            print article.get_url()

            try:
                urls.append((feedtitle, title, article.get_url(),None))
            except Exception as e:
                print 'get article error [%s] : %s'%(title, str(e))
                continue    

        return urls


# error articles 

# get article error [Miley Cyrus Cancels 2nd Concert After Hospitalization] : 'NoneType' object has no attribute '__getitem__'
# get article error [Developers Expect to Become Wealthy] : 'NoneType' object has no attribute '__getitem__'
# get article error [Deadly Virus Surges Through Arab Gulf] : 'NoneType' object has no attribute '__getitem__' (changed article name)
# Coeure sets out contours of possible ECB asset-buy plan
# Blackberry plans Heartbleed patches as mobile threat scrutinized

class main(object):
    
    urls = Shanbay().ParseFeedUrls()

    print urls

if __name__ == '__main__':
    main()