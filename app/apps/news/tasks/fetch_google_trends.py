from datetime import datetime
from datetime import timedelta

from celery import Task
from django.db.utils import IntegrityError

from config.celery import app
from src.trends.google import GoogleTrendsCrawler


class SyncGoogleTrends(Task):
    ignore_result = True
    name = 'sync_google_trends'

    def run(self, *args, **kwargs):
        from apps.news.models import GoogleTrend

        if GoogleTrend.objects.count() > 0:
            current_date = datetime.now().strftime(GoogleTrendsCrawler.date_format)
            self.__sync_date_trends(current_date)

            return

        dates_for_past_trends = [datetime.now() - timedelta(days=i) for i in range(7)]
        dates_for_past_trends = [date.strftime(GoogleTrendsCrawler.date_format) for date in dates_for_past_trends]
        for date in dates_for_past_trends:
            self.__sync_date_trends(date)

    @staticmethod
    def __sync_date_trends(date: str):
        from apps.news.models import GoogleTrend

        crawler = GoogleTrendsCrawler(date_string=date)
        date_trends = crawler()

        if not date_trends:
            return

        for trend_meta in date_trends:
            trend: GoogleTrend = GoogleTrend()
            trend.title = trend_meta['title']
            trend.source = trend_meta['source']
            trend.url = trend_meta['url']
            trend.query = trend_meta['query']
            trend.trended_at = datetime.strptime(date, crawler.date_format)
            try:
                trend.save()
            except IntegrityError as error:
                continue


app.register_task(SyncGoogleTrends())
