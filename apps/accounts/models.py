from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models import Q, Sum
from django.utils import timezone
import jdatetime
import os

from TopLearn.settings import MEDIA_ROOT


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, active_code=None, image_name=None, password=None):
        if not username:
            raise ValueError("نام کاربری را وارد کنید!")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            active_code=active_code,
            image_name=image_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, active_code=None, image_name=None):
        user = self.create_user(
            username=username,
            email=email,
            active_code=active_code,
            image_name=image_name,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ============================================================================================


def upload_user_image(instance, filename):
    filename, ext = os.path.splitext(filename)
    return f"images/UserAvatar/{uuid4()}{ext}"


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    active_code = models.CharField(max_length=50, blank=True, null=True,verbose_name='کد فعال سازی')
    image_name = models.ImageField(upload_to=upload_user_image, null=True, blank=True, verbose_name='آواتار')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت(فعال/غیرفعال)')
    register_date = models.DateField(default=timezone.now)
    is_admin = models.BooleanField(default=False, verbose_name='مدیر')
    is_superuser = models.BooleanField(default=False, verbose_name='مدیرکل')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}  {self.email}"

    @property
    def is_staff(self):
        return self.is_admin


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def get_register_date_shamsi(self):
        jdatetime_obj = jdatetime.datetime.fromgregorian(datetime=self.register_date)
        return jdatetime_obj.strftime('%Y/%m/%d')

    def set_image(self, image):
        if self.image_name is not None:
            image_path = MEDIA_ROOT + 'media/images/UserAvatar/' + str(self.image_name)
            if os.path.exists(image_path):
                os.remove(image_path)
        self.image_name = image

    def get_wallets_user(self):
        return self.wallets_of_user.filter(is_pay=True)

    def balance_wallet(self):
        enter = self.wallets_of_user.filter(Q(type__type_id=1) & Q(is_pay=True)).aggregate(Sum('amount'))['amount__sum']
        if enter is None:
            enter = 0
        exit = self.wallets_of_user.filter(Q(type__type_id=2) & Q(is_pay=True)).aggregate(Sum('amount'))['amount__sum']
        if exit is None:
            exit = 0

        return (enter - exit)


