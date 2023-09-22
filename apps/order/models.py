import jdatetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.accounts.models import User
from apps.course.models import Course
from enum import Enum


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="کاربر")
    order_sum = models.IntegerField(verbose_name="جمع فاکتور")
    is_finaly = models.BooleanField(default=False, verbose_name="وضعیت نهایی شده")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت فاکتور')

    def __str__(self):
        return self.user.username + str(self.id)

    def get_created_date_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.created_date)
        return jdatetime_obj.strftime('%Y/%m/%d ساعت %H')

    class Meta:
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتور ها'
        db_table = 't_orders'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details', verbose_name='فاکتور')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_details', verbose_name='دوره')
    count = models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت')

    def __str__(self):
        return self.order + ' ' + self.course.courseTitle

    class Meta:
        verbose_name = 'ریزفاکتور'
        verbose_name_plural = 'ریزفاکتور ها'
        db_table = 't_order_details'


class Discount(models.Model):
    discount_code = models.CharField(max_length=150, verbose_name='کد تخفیف')
    discount_percent = models.IntegerField(verbose_name='درصد تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    usable_count = models.IntegerField(null=True, blank=True, verbose_name='تعداد استفاده')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='شروع استفاده')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='پایان استفاده')

    def __str__(self):
        return f"کد تخفیف : {self.discount_code} ,درصد تخفیف : {self.discount_percent}"

    def get_start_date_shamsi(self):
        if self.start_date is not None:
            jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.start_date)
            return jdatetime_obj.strftime('%Y/%m/%d')
        else:
            return "-"

    def get_end_date_shamsi(self):
        if self.end_date is not None:
            jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.end_date)
            return jdatetime_obj.strftime('%Y/%m/%d')
        else:
            return "-"

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'
        db_table = 't_discounts'


class UserDiscountCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discounts', verbose_name='کاربر')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='userdiscounts', verbose_name='تخفیف')

    def __str__(self):
        return self.user + ' ' + str(self.discount)

    class Meta:
        db_table = 't_user_discounts'


class DiscountUseType(Enum):
    Success = 1
    ExpiredDate = 2
    NotFound = 3
    Finished = 4
    UserUsed = 5
