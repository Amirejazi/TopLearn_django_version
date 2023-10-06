from django.urls import path
from .views import CreateQuestion, ListQuestion, ShowQuestion, AddAnswer, SelectIsTrueAnswer

app_name = 'forum'
urlpatterns = [
    path('add_question/<int:course_id>', CreateQuestion.as_view(), name='CreateQuestion'),
    path('', ListQuestion.as_view(), name='ListQuestion'),
    path('show_question/<int:question_id>', ShowQuestion.as_view(), name='ShowQuestion'),
    path('add_answer/', AddAnswer.as_view(), name='AddAnswer'),
    path('select_true_answer', SelectIsTrueAnswer.as_view(), name='SelectIsTrueAnswer'),
]
