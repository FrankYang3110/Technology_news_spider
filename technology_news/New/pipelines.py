# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
from MySQLdb.cursors import DictCursor


class NewPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        params= dict(host=crawler.settings.get('HOST'),
                     user=crawler.settings.get('USER'),
                     passwd=crawler.settings.get('PASSWORD'),
                     db=crawler.settings.get('DB'),
                     charset='utf8',
                     use_unicode=True,
                     cursorclass=DictCursor,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **params)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_into, item)
        query.addErrback(self.handle_failure, item, spider)

    def handle_failure(self, failure, item, spider):
        print(failure)

    def insert_into(self, cursor, item):
        insert_sql = """
        INSERT INTO news(title, url, text, source, time)
        VALUES(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE
        text=VALUES(text), source=VALUES(source), time=VALUES(time)
        """
        cursor.execute(insert_sql, (item['title'],item['url'],item['text'],item['source'],item['time']))





