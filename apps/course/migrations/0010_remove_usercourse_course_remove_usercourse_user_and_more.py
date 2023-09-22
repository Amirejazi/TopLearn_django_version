# Generated by Django 4.2.4 on 2023-09-16 01:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0009_usercourse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercourse',
            name='course',
        ),
        migrations.RemoveField(
            model_name='usercourse',
            name='user',
        ),
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ManyToManyField(related_name='users_in_course', to=settings.AUTH_USER_MODEL, verbose_name='کاربرانی که دوره رو تهیه کردن'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['-createDate'], name='t_courses_createD_3572d4_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['-updateDate'], name='t_courses_updateD_6b4123_idx'),
        ),
        migrations.DeleteModel(
            name='UserCourse',
        ),
    ]
