from django.db import migrations
from django.contrib.auth.management import create_permissions

def rename_permission(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    permission = Permission.objects.get(codename='change_wallet')
    permission.name = 'تغییر کیف پول'
    permission.save()


class Migration(migrations.Migration):

    dependencies = [
        ('userpanel', '0003_alter_wallet_options'),
    ]

    operations = [
        migrations.RunPython(rename_permission),
    ]
