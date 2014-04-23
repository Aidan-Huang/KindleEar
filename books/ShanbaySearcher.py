#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib, urllib2 
from bs4 import BeautifulSoup
import simplejson

class ShanbayNews(object):
    """An article of news in Shanbay"""
    def __init__(self, title, source, date):
        self.title = title
        self.source = source
        self.date = date

        if 'feeds.reuters.com' == source:
            self.search = ReutersSearcher()
            self.source = "reuters.com"

        elif 'voanews.com' == source:
            self.search = VOASearcher()
        

    def get_url(self):
        
        return self.search.get_url(self.title)


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

        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&safe=active&%s' % (query)


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

        # print VOASearcher.site + VOASearcher.search_url + query

        d = urllib2.urlopen(VOASearcher.site + VOASearcher.search_url + query)

        soup = BeautifulSoup(d.read().decode('utf-8'))


        try:

            url = soup.find('a', attrs = {'class': 'linkmed'})['href']
            url = VOASearcher.site + url

            return url

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
    

        d = urllib2.urlopen(ReutersSearcher.site + ReutersSearcher.search_url + query)

        soup = BeautifulSoup(d.read().decode('utf-8'))

        
        try:
                
            url = soup.find('li', attrs = {'class': 'searchHeadline'}).a
            url = url['href']

            return url

        except Exception as e:
            raise SearchException("ReutersSearcher error:" + str(e)) 
  

class ShanbaySearcher(object):
    
    @staticmethod
    def search():
    
        url = 'http://www.Shanbay.com/read/news/'
        urls = []
    
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
        
            #print article.get_url()
    
            try:
                urls.append(('ShanbayNews', title, article.get_url(),None))
            # except SearchException as e:
            #     print 'get article error [%s] : %s' % (title, str(e))
            #     continue
            except Exception as e:
                print 'errer, now try GoogleSearcher:[%s] : %s' % (title, str(e))

                try:
                    url = GoogleSearcher.get_url(title, article.source)
                    urls.append(('ShanbayNews', title, url, None))

                except exception as e:
                    print "no results:" + title

                continue    
    
        return urls

# error articles 

# get article error [Miley Cyrus Cancels 2nd Concert After Hospitalization] : 'NoneType' object has no attribute '__getitem__'
# get article error [Developers Expect to Become Wealthy] : 'NoneType' object has no attribute '__getitem__'
# get article error [Deadly Virus Surges Through Arab Gulf] : 'NoneType' object has no attribute '__getitem__' (changed article name)
# Coeure sets out contours of possible ECB asset-buy plan
# Blackberry plans Heartbleed patches as mobile threat scrutinized
# get article error [Study: Processed Meat Raises Colorectal Cancer Risk] : 'NoneType' object has no attribute '__getitem__'
# get article error [Colombian Novelist Garcia Marquez Dies at 87] : 'NoneType' object has no attribute '__getitem__'
# get article error [Scientists Create Highly Efficient Thermoelectric Material] : 'NoneType' object has no attribute '__getitem__'
# get article error [Bank of America's financial crisis costs become a recurring nightmare] : 'NoneType' object has no attribute 'a'


class main(object):

    voa = "www.voanews.com"
    reuters = "reuters.com"

    # title = "Study: Processed Meat Raises Colorectal Cancer Risk"
    # result_url = 'http://www.voanews.com/content/study-processed-meat-raises-colorectal-cancer-risk/1895891.html'    
    # print GoogleSearcher.get_url(title, voa) #== result_url

    # title = "Colombian Novelist Garcia Marquez Dies at 87"
    # result_url = 'http://www.voanews.com/content/colombian-novelist-garcia-marquez-dies-at-87/1895828.html'    
    # print GoogleSearcher.get_url(title, voa) #result_url == result_url

    # title = "Scientists Create Highly Efficient Thermoelectric Material"
    # result_url = 'http://www.voanews.com/content/scientists-create-highly-efficient-thermoelectric-material/1895867.html'    
    # print VOASearcher.get_url(title) #== result_url

    # title = "Bank of America's financial crisis costs become a recurring nightmare"
    # result_url = 'http://www.reuters.com/article/idUSBREA3F24B20140416'    
    # print ReutersSearcher.get_url(title) #== result_url

    # title = "Wall Street Week Ahead: Spring fever brings hope for U.S. earnings"
    # result_url = 'http://www.reuters.com/article/idUSBREA3F24B20140416'    
    # print ReutersSearcher.get_url(title) == result_url 

    # missing article
    # title = "In a cloning first, scientists create stem cells from adults"
    # result_url = 'http://www.reuters.com/article/idUSBREA3F24B20140416'    
    # print ReutersSearcher.get_url(title) #== result_url 


    # str = '<p>No results were found.</p>'
    # soup = BeautifulSoup(str)
    
    # noResult = soup.find(text='No results were found.')
    # print noResult == None


    # print ShanbaySearcher.search()

    print "hello world"


# if __name__ == '__main__':
#     main()