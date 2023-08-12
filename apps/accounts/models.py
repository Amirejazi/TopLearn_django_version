from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


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
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    active_code = models.CharField(max_length=50, blank=True, null=True)
    image_name = models.ImageField(upload_to="", null=True, blank=True, verbose_name='آواتار')
    is_active = models.BooleanField(default=False)
    register_date = models.DateField(default=timezone.now)
    is_admin = models.BooleanField(default=False)

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
