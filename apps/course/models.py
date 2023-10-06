import os
from uuid import uuid4
import jdatetime
from admin_decorators import short_description
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from sorl.thumbnail import get_thumbnail
from TopLearn.settings import MEDIA_ROOT
from apps.accounts.models import User
from .utils import compact_and_resize_image


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
    description = RichTextUploadingField(config_name='super', verbose_name='شرح دوره')
    price = models.PositiveIntegerField(verbose_name='قیمت دوره')
    tags = models.CharField(max_length=500, verbose_name='کلمات کلیدی')
    courseImageName = models.ImageField(upload_to=upload_course_image, verbose_name='تصویر دوره')
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    demoFileName = models.FileField(upload_to=upload_course_demo, verbose_name='ویدیو دمو دوره')
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='courses_of_group', verbose_name='گروه اصلی')
    subGroup = models.ForeignKey(CourseGroup, null=True, blank=True, on_delete=models.CASCADE, related_name='courses_of_subgroup', verbose_name='گروه فرعی')
    courseStatus = models.ForeignKey(CourseStatus, on_delete=models.CASCADE, related_name='courses_of_status', verbose_name='وضعیت دوره')
    courseLevel = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name='courses_of_level', verbose_name='سطح دوره')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_of_teacher', verbose_name='مدرس')
    user = models.ManyToManyField(User, related_name='courses_of_user', verbose_name='کاربرانی که دوره رو تهیه کردن')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت (فعال/غیرفعال)')

    def __str__(self):
        return f"نام دوره: {self.courseTitle}"

    @property
    def base_courseImageName(self):
        return os.path.basename(self.courseImageName.name)

    def get_createDate_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.createDate)
        return jdatetime_obj.strftime('%Y/%m/%d')

    @short_description('آخرین بروزرسانی')
    def get_updateDate_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.updateDate)
        return jdatetime_obj.strftime('%Y/%m/%d')

    class Meta:
        permissions = [
            ("master_panel", "پنل مدرس")
        ]
        indexes = [
            models.Index(fields=['-createDate']),
            models.Index(fields=['-updateDate']),
        ]
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
        compact_and_resize_image(course.courseImageName, 200)
    #thumbnail = get_thumbnail(course.courseImageName, '200x150', quality=99, format='JPEG')
    # thumbnail.save('/path/to/save/thumbnail.jpg')


@receiver(pre_delete, sender=Course)
def image_delete_handler(sender, instance, *args, **kwargs):
    if instance.courseImageName:
        instance.courseImageName.delete()
    if instance.demoFileName:
        instance.demoFileName.delete()

## Episode Model ================================================================================================


def upload_episode_file(instance, filename):
    return f"coursefiles/{filename}"


class Episode(models.Model):
    episodeTitle = models.CharField(max_length=150, verbose_name='عنوان قسمت')
    episodeTime = models.DurationField(verbose_name='زمان')
    is_free = models.BooleanField(default=False, verbose_name='رایگان بودن')
    episodefilename = models.FileField(upload_to=upload_episode_file, verbose_name='فایل قسمت')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='episodes', verbose_name='دوره مربوطه')

    def __str__(self):
        return self.episodeTitle

    def save(self, *args, **kwargs):
        try:
            episode = Episode.objects.get(id=self.id)
            if os.path.exists(MEDIA_ROOT + str(episode.episodefilename)) and self.episodefilename and (episode.episodefilename != self.episodefilename):
                episode.episodefilename.delete(save=False)
        except Episode.DoesNotExist:
            pass
        super(Episode, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'قسمت'
        verbose_name_plural = 'قسمت ها'
        db_table = 't_episodes'


class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name='دوره')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر ثبت کننده نظر')
    comment = models.TextField(max_length=700, verbose_name='متن نظر')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت نظر')
    is_admin_read = models.BooleanField(default=False, verbose_name='دیده شدن توسط ادمین')

    def __str__(self):
        return f"نظر کاربر {self.user.username} برای دوره {self.course.courseTitle}"

    def get_created_date_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.created_date)
        return jdatetime_obj.strftime('%Y/%m/%d')

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'نظر'
        verbose_name_plural = 'نظر ها'
        db_table = 't_comments'


class CourseVote(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='vote', verbose_name='دوره')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote', verbose_name='کاربر ثبت کننده لایک')
    vote = models.BooleanField(default=False, verbose_name='وضعیت پسندیدن')
    vote_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')

    def __str__(self):
        return f"وضعیت پسندیدن کاربر {self.user.username} برای دوره {self.course.courseTitle}"

    class Meta:
        verbose_name = 'پسند'
        verbose_name_plural = 'پسند ها'
        db_table = 't_votes'
