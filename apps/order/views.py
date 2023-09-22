from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseBadRequest
from apps.order.models import Order
from apps.order.utils import finally_order, use_discount


class ShowOrder(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            order = Order.objects.get(Q(user=user) & Q(id=kwargs['order_id']))
            context = {
                'order': order,
                'finaly': request.GET.get('finaly'),
                'discount_type': request.GET.get('type'),
            }
            return render(request, 'Order_app/ShowOrder.html', context)
        except Order.DoesNotExist:
            return HttpResponseNotFound()


class FinallyOrder(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        order_id = kwargs.get('order_id')
        if finally_order(user, order_id):
            return redirect(f'/order/show_order/{order_id}?finaly=true')
        else:
            return HttpResponseBadRequest()


class UseDiscount(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('orderId')
        discount_code = request.POST.get('code')
        try:
            order = Order.objects.get(id=order_id)
            type = use_discount(order, discount_code)
            return redirect(f'/order/show_order/{order_id}?type={type}')
        except Order.DoesNotExist:
            return HttpResponseNotFound()


class OrdersList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user)
        return render(request, 'Order_app/OrdersList.html', {'orders': orders})
