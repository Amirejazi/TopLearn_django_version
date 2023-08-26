import os
from uuid import uuid4
from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from sorl.thumbnail import get_thumbnail

from TopLearn.settings import MEDIA_ROOT
from apps.accounts.models import User
from apps.course.utils import compact_and_resize_image


class CourseGroup(models.Model):
    groupTitle = models.CharField(max_length=200, verbose_name='عنوان گروه')
    parent = models.ForeignKey("CourseGroup", blank=True, null=True, on_delete=models.CASCADE, related_name='SubGroups', verbose_name=' گروه والد')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت (فعال/غیرفعال)')

    def __str__(self):
        return self.groupTitle

    class Meta:
        verbose_name = 'گروه دوره ها'
        verbose_name_plural = 'گروه های دوره ها'
        db_table = 't_course_groups'


class CourseStatus(models.Model):
    statusTitle = models.CharField(max_length=150, verbose_name='عنوان وضعیت دوره')

    def __str__(self):
        return self.statusTitle

    class Meta:
        verbose_name = 'وضعیت دوره'
        verbose_name_plural = 'وضعیت دوره'
        db_table = 't_course_status'


class CourseLevel(models.Model):
    levelTitle = models.CharField(max_length=150, verbose_name='عنوان سطح دوره')

    def __str__(self):
        return self.levelTitle

    class Meta:
        verbose_name = 'سطح دوره'
        verbose_name_plural = 'سطح دوره'
        db_table = 't_course_level'


def upload_course_image(instance, filename):
    filename, ext = os.path.splitext(filename)
    path_output = f"images/course/image/{uuid4()}{ext}"
    try:
        course = Course.objects.get(id=instance.id)
        if course.courseImageName is not None:
            image_path = MEDIA_ROOT + str(course.courseImageName)
            if os.path.exists(image_path):
                os.remove(image_path)
        return path_output
    except Course.DoesNotExist:
        return path_output


def upload_course_demo(instance, filename):
    filename, ext = os.path.splitext(filename)
    try:
        course = Course.objects.get(id=instance.id)
        if course.demoFileName is not None:
            demo_path = MEDIA_ROOT + str(course.demoFileName)
            if os.path.exists(demo_path):
                os.remove(demo_path)
        return f"images/course/demos/{uuid4()}{ext}"
    except Course.DoesNotExist:
        return f"images/course/demos/{uuid4()}{ext}"


class Course(models.Model):
    courseTitle = models.CharField(max_length=200, verbose_name='عنوان دوره')
    description = models.TextField(max_length=650, verbose_name='شرح دوره')
    price = models.PositiveIntegerField(verbose_name='قیمت دوره')
    tags = models.CharField(max_length=500, verbose_name='کلمات کلیدی')
    courseImageName = models.ImageField(upload_to=upload_course_image, verbose_name='تصویر دوره')
    createDate = models.DateField(auto_now_add=True, verbose_name='تاریخ درج')
    updateDate = models.DateField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    demoFileName = models.FileField(upload_to=upload_course_demo, verbose_name='ویدیو دمو دوره')
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='courses_of_group', verbose_name='گروه اصلی')
    subGroup = models.ForeignKey(CourseGroup, null=True, blank=True, on_delete=models.CASCADE, related_name='courses_of_subgroup', verbose_name='گروه فرعی')
    courseStatus = models.ForeignKey(CourseStatus, on_delete=models.CASCADE, related_name='courses_of_status', verbose_name='وضعیت دوره')
    courseLevel = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name='courses_of_level', verbose_name='سطح دوره')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_of_user', verbose_name='مدرس')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت (فعال/غیرفعال)')

    def __str__(self):
        return self.courseTitle + ' ' + str(self.teacher)

    @property
    def base_courseImageName(self):
        return os.path.basename(self.courseImageName.name)

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'
        db_table = 't_courses'

    # def save(self, *args, **kwargs):
    #     if self.courseImageName:
    #         self.courseImageName = get_thumbnail(self.courseImageName, '500x600', quality=99, format='JPEG')
    #     super(MyPhoto, self).save(*args, **kwargs)


@receiver(post_save, sender=Course)
def thumbnail_creator(sender, instance, *args, **kwargs):
    course = Course.objects.get(id=instance.id)
    if instance.courseImageName:
        compact_and_resize_image(instance.courseImageName, 200)
    #thumbnail = get_thumbnail(course.courseImageName, '200x150', quality=99, format='JPEG')
    # thumbnail.save('/path/to/save/thumbnail.jpg')



@receiver(pre_delete, sender=Course)
def image_delete_handler(sender, instance, *args, **kwargs):
    if instance.courseImageName:
        instance.courseImageName.delete()
    if instance.demoFileName:
        instance.demoFileName.delete()

## Episode Model ================================================================================================

class Episode(models.Model):
    episodeTitle = models.CharField(max_length=150, verbose_name='عنوان قسمت')
    episodeTime = models.TimeField(verbose_name='زمان')
    is_free = models.BooleanField(default=False, verbose_name='رایگان بودن')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='episodes', verbose_name='دوره مربوطه')

    def __str__(self):
        return self.episodeTitle

    class Meta:
        verbose_name = 'قسمت'
        verbose_name_plural = 'قسمت ها'
        db_table = 't_episodes'
