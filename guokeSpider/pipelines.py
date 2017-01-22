# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import datetime
import pymysql
import re
from pymysql.err import MySQLError

today = datetime.datetime.now().date().isoformat()

class JsonWriterPipeline(object):
    def __init__(self):
        self.today = today
    def open_spider(self, spider):
        self.file = codecs.open('%s_export_%s.jl' % (spider.name, self.today), 'w+', encoding='utf-8')
    def close_spider(self, spider):
        self.file.close()
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode('utf-8').decode('unicode_escape'))
        return item



class MysqlStorePipeline(object):
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_database, mysql_charset):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database
        self.mysql_charset = mysql_charset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_database=crawler.settings.get('MYSQL_DBNAME'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWD'),
            mysql_charset=crawler.settings.get('MYSQL_CHARSET'),
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.mysql_host,
                                    user=self.mysql_user,
                                    password=self.mysql_password,
                                    database=self.mysql_database,
                                    charset=self.mysql_charset,)
        self.set = self.getAll_items(spider)
        # spider.logger.debug('------------------------------already exist id '+ str(self.set))

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        id = item['articleId']
        spider.logger.debug('this item id is %s , and set is %s' % (id,self.set))
        if id not in self.set:
            self.insert_item(item, spider)
        else:
            spider.logger.debug('%s already exist' % item['articleId'])
        return item

    def insert_item(self, item, spider):
        spider.logger.debug('-------------start insert--------------')
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO `scientific` (`id`, `issueDate`, `label`, `subLabel`, `title`, `summary`, `url`)" \
                      "VALUES(%s, %s, %s, %s, %s, %s, %s);"
                values = (item['articleId'], item['publishDate'], item['label'], item['subLabel'], item['title'], item['summary'], item['articleUrl'])
                cursor.execute(sql, values)
            self.conn.commit()
        except MySQLError as e:
            spider.logger.debug("insert error" + str(e))

    def getAll_items(self, spider):
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT `id` FROM `scientific`"
                cursor.execute(sql, ())
                results = cursor.fetchall()
                return tuple([str(i) for (i,) in results])
        except MySQLError as e:
            spider.logger.debug()




