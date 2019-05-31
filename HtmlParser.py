# coding:utf-8
import  re
import urllib.parse
from bs4 import BeautifulSoup

class HtmlParser(object):

    def parser(self,page_url,html_cont):
        '''
        解析网页内容，抽取url和数据
        :param page_url: 下载页面的URL
        :param html_cont: 下载的网页内容
        :return:
        '''
        if page_url is None or html_cont is None:
            return
        soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return  new_urls,new_data

    def _get_new_urls(self,page_url,soup):
        '''
        抽取新的url
        :param page_url: 下载页面的url
        :param soup: soup
        :return:  返回新的url集合
        '''
        new_urls = set()
        #抽取符合要求的a标记
        links=soup.find_all('a',href=re.compile(r'/item/.*'))
        for link in links[5:-1] :
            #提取href属性
            new_url = link['href']
            #拼接完整url
            new_full_url =urllib.parse.urljoin('https://baike.baidu.com',new_url)
            new_urls.add(new_full_url)
        return  new_urls

    def _get_new_data(self,page_url,soup):
        '''
        抽取有效的数据
        :param page_url: 下载页面的url
        :param soup:
        :return: 返回有效数据
        '''
        data={}
        data['url']=page_url
        title = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title']=title.get_text()
        summary = soup.find('div',class_='para')
        data['summary'] = summary.get_text()

        return  data

