from celery import Task
from scrapy.crawler import CrawlerProcess

from config.celery import app
from src.crawlers.ua_news.spider import UANewsSpider


class SyncUANews(Task):
    ignore_result = True
    name = 'sync_112ua_news'

    def run(self, *args, **kwargs):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(UANewsSpider)
        process.start(stop_after_crawl=False)


app.register_task(SyncUANews())
