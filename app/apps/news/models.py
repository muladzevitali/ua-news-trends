from datetime import datetime, timedelta

from django.db import models
from django.db.models.signals import (pre_save, post_save)
from src.utils import clean_title


class GoogleTrend(models.Model):
    title = models.CharField(max_length=1000)
    source = models.CharField(max_length=1000)
    url = models.CharField(unique=True, max_length=1000)
    query = models.CharField(max_length=1000)
    trended_at = models.DateField()

    facet = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def sync_trending_status(sender, instance: 'GoogleTrend', **kwargs):
        if not instance.facet and instance.title:
            instance.facet = clean_title(instance.title)
            instance.save()

        news_list = News.objects.filter(facet__iregex=instance.facet)
        for news in news_list:
            news.is_trending = True
            news.trended_query = instance.title
            news.save()

    def __str__(self):
        return f'Trend: {self.title} - {self.url}'


class News(models.Model):
    title = models.CharField(max_length=1000)
    url = models.CharField(unique=True, max_length=1000)
    published_at = models.DateTimeField()
    category = models.CharField(max_length=100, null=True)
    is_trending = models.BooleanField(default=False)
    image_url = models.CharField(null=True, max_length=1000)
    trended_query = models.CharField(max_length=1000, null=True)

    facet = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def sync_trending_status(sender, instance: 'News', **kwargs):
        trended_from = datetime.now().date() - timedelta(days=8)

        if not instance.facet:
            instance.facet = clean_title(instance.title)
            instance.save()

        if instance.is_trending:
            return

        trended_news = GoogleTrend.objects.filter(facet__iregex=instance.facet, trended_at__gte=trended_from)
        if trended_news.count():
            instance.is_trending = True
            instance.trended_query = trended_news.first().title
            instance.save()

    def __str__(self):
        return f'News: {self.title} - {self.url}'


post_save.connect(GoogleTrend.sync_trending_status, sender=GoogleTrend)
pre_save.connect(News.sync_trending_status, sender=News)
