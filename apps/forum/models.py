import jdatetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from apps.accounts.models import User
from apps.course.models import Course


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions', verbose_name='دوره مرتبط سوال')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name='سوال کننده')
    title = models.CharField(max_length=400, verbose_name='عنوان سوال')
    body = RichTextUploadingField(config_name='normal', verbose_name='شرح سوال')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.title

    def get_created_date_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.created_date)
        return jdatetime_obj.strftime('%Y/%m/%d')

    def get_modified_date_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.modified_date)
        return jdatetime_obj.strftime('%Y/%m/%d')

    class Meta:
        ordering = ('-modified_date',)
        indexes = [
            models.Index(fields=['course']),
        ]
        verbose_name = 'سوال'
        verbose_name_plural = 'سوال ها'
        db_table = 't_questions'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='سوال مرتبط')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', verbose_name='جواب دهنده')
    answer_body = RichTextUploadingField(config_name='super', verbose_name='شرح جواب')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_true = models.BooleanField(default=False, verbose_name='وضعیت درست بودن')

    def __str__(self):
        return f"جواب سوال :{self.question.title} توسط :{self.user.username}"

    def get_created_date_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.created_date)
        return jdatetime_obj.strftime('%Y/%m/%d')

    class Meta:
        ordering = ('-created_date',)
        indexes = [
            models.Index(fields=['question']),
        ]
        verbose_name = 'جواب'
        verbose_name_plural = 'جواب ها'
        db_table = 't_answers'
