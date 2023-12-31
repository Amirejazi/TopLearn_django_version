# Generated by Django 4.2.4 on 2023-10-03 12:06

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0014_coursevote'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='عنوان سوال')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='شرح سوال')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='course.course', verbose_name='دوره مرتبط سوال')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='سوال کننده')),
            ],
            options={
                'verbose_name': 'سوال',
                'verbose_name_plural': 'سوال ها',
                'db_table': 't_questions',
                'ordering': ('-modified_date',),
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='شرح جواب')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('is_true', models.BooleanField(default=False, verbose_name='وضعیت درست بودن')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='forum.question', verbose_name='سوال مرتبط')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL, verbose_name='جواب دهنده')),
            ],
            options={
                'verbose_name': 'جواب',
                'verbose_name_plural': 'جواب ها',
                'db_table': 't_answers',
                'ordering': ('-created_date',),
            },
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['course'], name='t_questions_course__594072_idx'),
        ),
        migrations.AddIndex(
            model_name='answer',
            index=models.Index(fields=['question'], name='t_answers_questio_6888a0_idx'),
        ),
    ]
