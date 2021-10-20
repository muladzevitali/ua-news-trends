from .models import News


def news_categories(request):
    if 'admin' in request.path:
        return dict()

    categories = News.objects.order_by('category').values_list('category', flat=True).distinct()

    return dict(categories=set(categories))