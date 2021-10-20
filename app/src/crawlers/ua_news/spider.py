import logging
from datetime import datetime

import scrapy
from django.db.utils import IntegrityError
from scrapy_djangoitem import DjangoItem

from apps.news.models import News

MONTH_RU = ('янв', 'февр', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сент', 'окт', 'нояб', 'дек')
MONTH_EN = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')

WEEKDAYS_RU = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')
WEEKDAYS_EN = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')


def _ru_to_en_date_text(date_string: str) -> str:
    date_string = date_string.lower().replace('.', '')

    for ru_str, en_str in zip(MONTH_RU, MONTH_EN):
        date_string = date_string.replace(ru_str, en_str)

    for ru_str, en_str in zip(WEEKDAYS_RU, WEEKDAYS_EN):
        date_string = date_string.replace(ru_str, en_str)

    return date_string


class NewsItem(DjangoItem):
    django_model = News


class UANewsSpider(scrapy.Spider):
    name = 'ua_news'
    allowed_domains = ['112ua.tv']
    start_urls = ['https://112ua.tv/rsslist']
    __date_format = '%a, %d %b %Y %H:%M:%S %z'

    # def __init__(self, name, **kwargs):
    #     logger = logging.getLogger('ua_news_spider')
    #     logger.setLevel(logging.DEBUG)
    #
    #     super().__init__(name, **kwargs)

    def parse(self, response, **kwargs):
        rss_feeds = response.xpath('//div[@class="statpage-content"]/p/a/@href').extract()
        for rss_feed in rss_feeds:
            yield scrapy.Request(rss_feed, callback=self.parse_rss_page)

    def parse_rss_page(self, request):
        items = request.xpath('//item')
        print(items)
        for item in items:
            news_item = NewsItem()
            news_item['title'] = item.xpath('./title/text()').extract_first()
            news_item['url'] = item.xpath('./link/text()').extract_first()
            news_item['category'] = item.xpath('./category/text()').extract_first()
            news_item['image_url'] = item.xpath('./enclosure/@url').extract_first()
            published_at = item.xpath('./pubDate/text()').extract_first()
            published_at = _ru_to_en_date_text(published_at)
            if published_at:
                news_item['published_at'] = datetime.strptime(published_at, self.__date_format)
            try:
                news_item.save()
            except IntegrityError:
                print('error')
                continue
