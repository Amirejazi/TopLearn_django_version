# Generated by Django 4.2.4 on 2023-10-05 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_coursevote'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'permissions': [('master_panel', 'پنل مدرس')], 'verbose_name': 'دوره', 'verbose_name_plural': 'دوره ها'},
        ),
    ]