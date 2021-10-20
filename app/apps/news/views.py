from django.views.generic import ListView

from .models import News


class NewsListView(ListView):
    model = News
    template_name = 'news.html'
    paginate_by = 10
