# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider
from JavFree.items import JavfreeItem
import logging
import re

class JavFree(Spider):
    name='JavFreeSpider'
    base_url='https://javfree.me'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url='https://javfree.me/category/mosaic'
        yield Request(url, headers=self.headers)

    #     一层爬虫，抓取顶层目录，目录内为系列
    def parse(self, response):
        series=response.xpath('//div[@class="menu-nav-container"]/ul/li[1]/ul/li')
        for serie in series:
            category_url=serie.xpath('./a/@href').extract()[0]
            yield Request(url=category_url, callback=self.parse_category)

    def parse_category(self,response):
        movies = response.xpath('//div[@class="content-block clear"]/div')  # 选取所有包含class='content-block clear' 的div 属性的值里面的div元素
        for movie in movies:
            movie_url=movie.xpath('./h2/a/@href')
            #进入movie详情界面爬取详细信息
            if movie_url:
                yield Request(url=movie_url.extract()[0], callback=self.parse_movie)
        #翻页
        next_page_url=response.xpath('//div[@class="nav-links"]/a[@class="next page-numbers"]/@href').extract()[0]
        if next_page_url:
            yield Request(url=next_page_url,callback=self.parse_category)

    def parse_movie(self,response):
        item=JavfreeItem()
        item['name'] =response.xpath('//header[@class="entry-header"]/h1/text()').extract()[0]
        item['view'] =response.xpath('//header[@class="entry-header"]/div/span[@class="post-view"]/span/text()').extract()[0]
        item['id'] = response.xpath('//div[@class="entry-content"]/p/strong/text()').extract()[0]
        para=response.xpath('//div[@class="entry-content"]/p/text()').extract()
        item['date'] =para[0].split(u'：')[-1].strip() # 提取发售时间
        item['time']=re.findall(r'\d+',para[1])[0]     #提取影片时长
        item['actress'] = para[2].split(u'：')[-1].strip()  # 提取演员名称
        item['serie'] = para[4].split(u'：')[-1].strip()  # 提取演员名称
        item['image_urls']=response.xpath('//div[@class="entry-content"]/p/img/@src').extract()
        yield item












        pass




