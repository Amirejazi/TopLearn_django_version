import jdatetime
from django.db import models
from apps.accounts.models import User


class WalletType(models.Model):
    type_id = models.PositiveIntegerField(primary_key=True)
    type_title = models.CharField(max_length=150, verbose_name='عنوان نوع تراکنش')

    def __str__(self):
        return self.type_title

    class Meta:
        verbose_name = 'نوع تراکنش'
        verbose_name_plural = 'نوع تراکنش ها'
        db_table = 't_wallet_type'


class Wallet(models.Model):
    type = models.ForeignKey(WalletType, null=True, on_delete=models.CASCADE, related_name='wallets_of_wallet_type', verbose_name='نوع تراکنش')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='wallets_of_user', verbose_name='کاربر')
    amount = models.PositiveBigIntegerField(verbose_name='مبلغ')
    description = models.CharField(max_length=500, verbose_name='شرح')
    is_pay = models.BooleanField(default=False, verbose_name='تایید شده')
    created_date = models.DateField(auto_now_add=True, verbose_name='تاریخ و ساعت"')

    def __str__(self):
        return f"{self.user} {self.type__type_title}"

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول ها'
        db_table = 't_wallets'

    def get_created_date_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.created_date)
        return jdatetime_obj.strftime('%Y/%m/%d')
