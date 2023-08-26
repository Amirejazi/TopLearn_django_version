from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('username', 'email', 'is_active', 'is_admin', 'get_register_date_shamsi')
    list_filter = ('is_active', 'is_admin')
    list_editable = ('is_active',)
    search_fields = ('username', 'email')
    ordering = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions')
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2',)}),
        ('دسترسی ها', {'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')})
    )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password','image_name')}),
        ('اطلاعات امنیتی', {'fields': ('active_code',)}),
        ('دسترسی ها',  {"classes": ["collapse"], 'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')})
    )
