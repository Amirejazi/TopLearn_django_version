from django.contrib import admin
from apps.order.models import Discount, OrderDetail, Order


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_code', 'discount_percent', 'usable_count', 'get_start_date_shamsi', 'get_end_date_shamsi')
    search_fields = ('discount_code', 'discount_percent')
    ordering = ('discount_percent',)


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetail
    extra = 3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_sum', 'is_finaly', 'get_created_date_shamsi')
    ordering = ('created_date',)
    list_editable = ['is_finaly']
    inlines = [OrderDetailsInline]
