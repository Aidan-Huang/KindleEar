#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import urlparse
import copy
import tempfile
import os
import time
from datetime import datetime, date
from base import BaseFeedBook
import urllib, urllib2 
from bs4 import BeautifulSoup
import simplejson

def getBook():
    return Shanbay

class Shanbay(BaseFeedBook):
# class Shanbay():

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

        urls = []

        news = ShanbayNews.getTodayNews()
    
        news = ShanbayNews.today(news)
    
        for a_news in news:
            
            url = ''
    
            title = a_news.title
    
            try:
                url = a_news.get_url()
            except Exception as e:
                print 'errer, now try GoogleSearcher:[%s] : %s' % (title, str(e))
                try:
                    url = GoogleSearcher.get_url(title, a_news.source)
                    
                except exception as e:
                    print "no results:" + title
                continue   

            title = a_news.source.replace('www.', '').replace('.com', ': ') + title
            urls.append(('Shanbay', title, url, None))
    
        return urls




class ShanbayNews(object):
    """An article of news in Shanbay"""

    global str_date_format 

    str_date_format = '%m/%d %Y'

    def __init__(self, title, source, date):
        self.title = title
        self.source = source
        self.date = date


        if 'feeds.reuters.com' == source:
            self.search = ReutersSearcher()
            self.source = "www.reuters.com"

        elif 'voanews.com' == source:
            self.search = VOASearcher()
        

    def get_url(self):
        
        return self.search.get_url(self.title)

    @staticmethod
    def today(news):

        r_news = []

        today = date.today()
        str_today = today.strftime(str_date_format)

        for a_news in news:
            if(str_today == a_news.date):
                r_news.append(a_news)

        return r_news

    @staticmethod
    def getTodayNews():

        url = 'http://www.Shanbay.com/read/news/'
    
        d = urllib2.urlopen(url)
    
        soup = BeautifulSoup(d.read().decode('utf-8'))
    
        r_news = []
    
        for article in soup.find_all('div', attrs = {'class': 'article'}):
            title = article.find('div', attrs = {'class': 'title'}).a.string
            info = article.find('div', attrs = {'class': 'info'}).find_all('span')
    
    
            source = info[0].string
            date = info[1].string
        
        
            news = ShanbayNews(title, source, date)

            r_news.append(news)

        return r_news


class SearchException(Exception):
    """fitting article exception"""
    pass

class NoResultsException(SearchException):
    pass

class URLSearcher(object):

    @staticmethod
    def get_url(title):
        pass

class GoogleSearcher:

    @staticmethod

    def get_url(title, source):

        qstr = title + " site:" + source

        query = urllib.urlencode({'q' : qstr})

        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&safe=off&%s' % (query)

        # print url

        try:

            search_results = urllib.urlopen(url)
        
            json = simplejson.loads(search_results.read())

            results = json['responseData']['results']

            return results[0]['url']

        except Exception as e:
            print 'get article error [%s] : %s' % (title, str(e))



class VOASearcher(URLSearcher):

    
    site = 'http://www.voanews.com'
    search_url = '/search/?'


    @staticmethod
    def get_url(title):

        query = urllib.urlencode({'k' : "\"" + title + "\""})

        try:

            d = urllib2.urlopen(VOASearcher.site + VOASearcher.search_url + query)

            soup = BeautifulSoup(d.read().decode('utf-8'))

            url = soup.find('a', attrs = {'class': 'linkmed'})['href']
        
            return VOASearcher.site + url

        except Exception as e:
            raise SearchException("VOASearcher error:" + str(e)) 
  

        
class ReutersSearcher(URLSearcher):


    site = 'http://www.reuters.com'
    search_url = '/search?'

    #Apple antitrust compliance off to a promising start: monitor
    #Apple+antitrust+compliance+off+to+a+promising+start%3A+monitor
   

    @staticmethod
    def get_url(title):

        query = urllib.urlencode({'blob' : "\"" + title + "\""})


        # print ReutersSearcher.site + '/search?' + query
    
        try:

            d = urllib2.urlopen(ReutersSearcher.site + ReutersSearcher.search_url + query)

            soup = BeautifulSoup(d.read().decode('utf-8'))
                
            url = soup.find('li', attrs = {'class': 'searchHeadline'}).a

            return url['href']

        except Exception as e:
            raise SearchException("ReutersSearcher error:" + str(e)) 
  


# class main():

#     print "start..."

#     shanbay = Shanbay()

#     print shanbay.ParseFeedUrls()

#     print "end..."


# if __name__ == '__main__':
#      main()