from django.urls import path
from .views import CourseGroupMenu, GetSubGroupsJson

app_name = 'course'
urlpatterns = [
    path('course_group_menu', CourseGroupMenu, name='CourseGroupMenu'),
    path('sub_groups_json/<int:id>', GetSubGroupsJson, name='GetSubGroupsJson'),
]