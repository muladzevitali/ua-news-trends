from django.urls import path

from . import views

urlpatterns = (
    path('', views.NewsListView.as_view(), name='news-list-view'),
    path('check_health/', views.health_check, name='health-check'),

)
