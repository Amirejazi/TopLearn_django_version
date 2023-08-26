from django.contrib import admin
from admin_decorators import short_description, order_field
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.actions import delete_selected
from django.core import serializers
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils.html import format_html

from apps.course.models import CourseGroup, Course, CourseStatus, CourseLevel


# CourseGroup Admin ====================================================================================


def deActive_productGroup(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} گروه غیرفعال شدند  '
    modeladmin.message_user(request, message)


def Active_productGroup(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} گروه فعال شدند  '
    modeladmin.message_user(request, message)


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = CourseGroup
    extra = 1


class GroupFilter(SimpleListFilter):
    title = 'گروه های اصلی'
    parameter_name = 'subgroup'

    def lookups(self, request, model_admin):
        sub_groups = CourseGroup.objects.filter(~Q(parent=None))
        groups = set([item.parent for item in sub_groups])
        return [(item.id, item.groupTitle) for item in groups]

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(Q(parent=self.value()))
        return queryset


@admin.register(CourseGroup)
class CourseGroupAdmin(admin.ModelAdmin):
    list_display = ('groupTitle', 'parent', 'count_sub_groups', 'count_courses_of_group', 'is_active')
    list_filter = (GroupFilter, 'is_active')
    search_fields = ('groupTitle',)
    ordering = ('parent', 'groupTitle',)
    inlines = [ProductGroupInstanceInlineAdmin]
    actions = [deActive_productGroup, Active_productGroup, export_as_json]
    list_editable = ['is_active']

    def get_queryset(self, *args, **kwargs):
        qs = super(CourseGroupAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(count_sub_groups=Count('SubGroups'))
        qs = qs.annotate(count_courses_of_group=Count('courses_of_group'))
        return qs

    @short_description('تعداد زیرگروه ها')
    @order_field('sub_groups')
    def count_sub_groups(self, obj):
        return obj.count_sub_groups

    @short_description('تعداد دوره ها')
    @order_field('courses_of_group')
    def count_courses_of_group(self, obj):
        return obj.count_courses_of_group

    deActive_productGroup.short_description = 'غیرفعال کردن گروه های انتخاب شده'
    Active_productGroup.short_description = 'فعال کردن گروه های انتخاب شده'
    delete_selected.short_description = 'حذف گروه های انتخاب شده'
    export_as_json.short_description = 'خروجی جیسون برای گروه های انتخاب شده'

## Course Admin ==================================================================================================

def DeActive_course(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} دوره غیرفعال شدند  '
    modeladmin.message_user(request, message)


def Active_course(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} دوره فعال شدند  '
    modeladmin.message_user(request, message)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseTitle', 'image_tag', 'courseStatus', 'price', 'updateDate', 'group', 'subGroup', 'teacher', 'is_active')
    list_filter = ('group', 'teacher', 'is_active')
    search_fields = ('courseTitle', 'group', 'subGroup', 'teacher', 'courseLevel')
    ordering = ('updateDate', 'courseTitle',)
    actions = [DeActive_course, Active_course, export_as_json]
    list_editable = ['is_active']

    deActive_productGroup.short_description = 'غیرفعال کردن کالا های انتخاب شده'
    Active_productGroup.short_description = 'فعال کردن کالا های انتخاب شده'

    @short_description('تصویر دوره')
    def image_tag(self, obj):
        return format_html(f'<img src="/media/images/course/thumb/{obj.base_courseImageName}"  />')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'subGroup':
            kwargs['queryset'] = CourseGroup.objects.filter(~Q(parent=None))
        if db_field.name == 'group':
            kwargs['queryset'] = CourseGroup.objects.filter(Q(parent=None))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ('اطلاعات دوره', {'fields': (
            'courseTitle',
            'price',
            'tags',
            ('group', 'subGroup'),
            'description',
            'courseStatus',
            'courseLevel',
            'courseImageName',
            'demoFileName',
            'teacher',
            'is_active'
        )}),
    )

    class Media:

        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',
        )


@admin.register(CourseStatus)
class CourseStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'statusTitle')
    search_fields = ('statusTitle',)


@admin.register(CourseLevel)
class CourseLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'levelTitle')
    search_fields = ('levelTitle',)
