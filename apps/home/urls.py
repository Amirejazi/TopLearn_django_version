from django.urls import path
from .views import *

app_name = 'home'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('error404', Error404.as_view(), name='Error404'),
    path('latest_courses/', latest_course, name='LatestCourses'),
    path('popular_courses', popular_courses, name='PopularCourses'),
    path('search_complete', search_complete, name='SearchComplete'),
]
