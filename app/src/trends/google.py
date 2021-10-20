import json
from datetime import datetime
from typing import (Optional, List)

import requests


class GoogleTrendsCrawler:
    date_format = '%Y%m%d'

    def __init__(self, date_string: Optional[str] = None):
        self.date_string = date_string or datetime.now().strftime('%Y%m%d')
        self.__base_url = 'https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=-240&ed=%s&geo=UA'
        self.url = self.__get_url(self.date_string)
        self.__response_json = dict()
        self.date_articles: List[dict] = list()

    def __get_url(self, date_string):
        return self.__base_url % date_string

    def __extract_date_trends(self):
        for day_data in self.__response_json['default'].get('trendingSearchesDays', []):
            if day_data['date'] == self.date_string:
                for trending_search in day_data['trendingSearches']:
                    query = trending_search['title']['query']
                    for article in trending_search['articles']:
                        article['query'] = query
                        self.date_articles.append(article)

                break

    def __call__(self, *args, **kwargs) -> dict:
        if kwargs.get('date_string'):
            self.date_string = kwargs['date_string']
            self.url = self.__get_url(self.date_string)

        response = requests.get(self.url)
        if not response.status_code == 200:
            raise ConnectionRefusedError('Can not get google trends for date')

        text = response.text.removeprefix(")]}',")
        self.__response_json = json.loads(text)
        self.__extract_date_trends()
        return self.date_articles
