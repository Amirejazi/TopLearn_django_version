from django.urls import path
from .views import ShowOrder, FinallyOrder, UseDiscount, OrdersList

app_name = 'order'
urlpatterns = [
    path('show_order/<int:order_id>', ShowOrder.as_view(), name='ShowOrder'),
    path('finaly_order/<int:order_id>', FinallyOrder.as_view(), name='FinallyOrder'),
    path('use_discount', UseDiscount.as_view(), name='UseDiscount'),
    path('orders_list', OrdersList.as_view(), name='OrdersList'),
]
