from django.urls import path
from .views import CourseGroupMenu, GetSubGroupsJson, CourseList, ShowCourse, BuyCourse, DownloadFiles, CreateComment, \
    show_comments, ShowCourseVote, add_vote

app_name = 'course'
urlpatterns = [
    path('course_group_menu', CourseGroupMenu, name='CourseGroupMenu'),
    path('sub_groups_json/<int:id>', GetSubGroupsJson, name='GetSubGroupsJson'),
    path('course_list', CourseList.as_view(), name='Courses'),
    path('show_course/<int:id>', ShowCourse.as_view(), name='ShowCourses'),
    path('buy_course/<int:course_id>', BuyCourse.as_view(), name='BuyCourses'),
    path('download_episodes/<int:episode_id>', DownloadFiles.as_view(), name='download_episodes'),
    path('create_comment/', CreateComment.as_view(), name='CreateComment'),
    path('show_comments/<int:course_id>', show_comments, name='ShowComments'),
    path('show_votes/<int:course_id>', ShowCourseVote.as_view(), name='ShowCourseVote'),
    path('add_vote/<int:course_id>', add_vote, name='AddVote'),
]
