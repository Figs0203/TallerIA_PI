from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('recommend/', views.recommend_view, name='recommend'),
]