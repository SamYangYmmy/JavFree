# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
from JavFree import settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from  dboperator import DBOperator
import MySQLdb
import MySQLdb.cursors

class JavfreePipeline(ImagesPipeline):
    dbpool = DBOperator()

    def get_media_requests(self, item, info):  # 重写ImagesPipeline   get_media_requests方法
        sql = ("INSERT INTO tbl_movie (id,movie_name, view_num, actress,pub_date,movie_time,tag,image_num)"
               "VALUES (%s, %s, %s , %s ,%s ,%s ,%s,%s )")
        self.dbpool.insert(sql,(item['id'],
                                item['name'],
                                int(item['view'].replace(u',','')),
                                item['actress'],
                                item['date'].replace('/','-'),
                                int(item['time']),
                                item['serie'],
                                len(item['image_urls'])))
        for image_url in item['image_urls']:
            meta = {'filename': u'%s/%s' % (item['actress'],image_url.split('/')[-1])}  # 将文件名通过item传入到meta里面，然后再file_path里面调用
            yield scrapy.Request(url=image_url, meta=meta)

    def file_path(self, request, response=None, info=None):
        image_guid = request.meta.get('filename', '')
        return '/%s' % (image_guid)

    def item_completed(self, results, item, info):
        '''当一个单独项目中的所有图片请求完成时（要么完成下载，要么因为某种原因下载失败），
         item_completed() 方法将被调用'''
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item