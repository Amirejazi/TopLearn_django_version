from django.db import migrations


def rename_permission(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    permission = Permission.objects.get(codename='add_wallet')
    permission.name = 'میتونه به کیف پول اضافه کنه'
    permission.save()
    permission = Permission.objects.get(codename='change_wallet')
    permission.name = 'میتونه کیف پول رو تغییر بده'
    permission.save()
    permission = Permission.objects.get(codename='delete_wallet')
    permission.name = 'میتونه کیف پول رو حذف کنه'
    permission.save()
    permission = Permission.objects.get(codename='view_wallet')
    permission.name = 'میتونه کیف پول هارو مشاهده کنه'
    permission.save()
    permission = Permission.objects.get(codename='add_wallettype')
    permission.name = 'میتونه به نوع تراکنش اضافه کنه'
    permission.save()
    permission = Permission.objects.get(codename='change_wallettype')
    permission.name = 'میتونه به نوع تراکنش را تغییر دهد'
    permission.save()
    permission = Permission.objects.get(codename='delete_wallettype')
    permission.name = 'میتونه نوع تراکنش را حذف کند'
    permission.save()
    permission = Permission.objects.get(codename='view_wallettype')
    permission.name = 'میتونه نوع تراکنش هارو مشاهده کنه'
    permission.save()
    permission = Permission.objects.get(codename='change_wallet')
    permission.name = 'تغییر کیف پول'
    permission.save()


class Migration(migrations.Migration):

    dependencies = [
        ('userpanel', '0004_auto_20230819_2134'),
    ]

    operations = [
        migrations.RunPython(rename_permission),
    ]
