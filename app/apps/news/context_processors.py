from .models import News


def news_categories(request):
    if 'admin' in request.path:
        return dict()

    categories = News.objects.values_list('category', flat=True).distinct()
    print(list(categories))
    return dict(categories=set(categories))