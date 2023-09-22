from django.urls import path
from .views import CourseGroupMenu, GetSubGroupsJson, CourseList, ShowCourse, BuyCourse

app_name = 'course'
urlpatterns = [
    path('course_group_menu', CourseGroupMenu, name='CourseGroupMenu'),
    path('sub_groups_json/<int:id>', GetSubGroupsJson, name='GetSubGroupsJson'),
    path('course_list', CourseList.as_view(), name='Courses'),
    path('show_course/<int:id>', ShowCourse.as_view(), name='ShowCourses'),
    path('buy_course/<int:course_id>', BuyCourse.as_view(), name='BuyCourses'),
]
