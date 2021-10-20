from django.views.generic import ListView

from .models import News


class NewsListView(ListView):
    model = News
    template_name = 'news.html'
    paginate_by = 10

    def get_queryset(self):
        query_set = self.model.objects.all()
        is_trending: str = self.request.GET.get('is_trending', False)
        if self.request.GET.get('is_trending', False) and is_trending.isdigit():
            is_trending = bool(int(is_trending))
            query_set = query_set.filter(is_trending=is_trending)

        return query_set
