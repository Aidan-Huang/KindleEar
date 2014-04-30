# colding:utf-8
import unittest
import time
from datetime import datetime, date
from books.Shanbay import ShanbayNews


class test(unittest.TestCase):

    def test(self):
        a = 10
        self.assertEqual(10, a)

        # today = date.today()
        # print today.year
        # print today.month
        # print today.day

        # str_date = '04/29 2014'
        # str_format = '%m/%d %Y'

        # dt = time.strptime(str_date, str_format)
        # dt = time.mktime(dt)
 
        # d = datetime.fromtimestamp(dt)

        # print d.strftime(str_format)
        # print today.strftime(str_format)



    def testFilterTodayNews(self):
        

        str_format = '%m/%d %Y'

        today = date.today()
        str_today = today.strftime(str_format)

        news1 = ShanbayNews('t1', 'voa', '04/28 2014')
        news2 = ShanbayNews('t2', 'voa', '04/29 2014')
        news3 = ShanbayNews('t2', 'voa', str_today)


        news = [news1, news2, news3]

        news = ShanbayNews.today(news)

        self.assertEqual(1, len(news))

        news4 = news[0]

        self.assertEqual(str_today, news4.date)


unittest.main()