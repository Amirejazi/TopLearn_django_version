# Generated by Django 4.2.4 on 2023-08-19 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpanel', '0002_alter_wallet_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'permissions': [('can_view', 'میتونه کیف پول را  تغییر دهد')], 'verbose_name': 'کیف پول', 'verbose_name_plural': 'کیف پول ها'},
        ),
    ]
