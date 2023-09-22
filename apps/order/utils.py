from datetime import datetime
from django.db.models import Q
from apps.order.models import Order, Discount, DiscountUseType, UserDiscountCode
from apps.userpanel.models import Wallet, WalletType


def finally_order(user, order_id):
    try:
        order = Order.objects.get(Q(user=user) & Q(id=order_id) & Q(is_finaly=False))
        if user.balance_wallet() >= order.order_sum:
            order.is_finaly = True
            order.save()
            Wallet.objects.create(
                user=user,
                type=WalletType.objects.get(type_id=2),
                amount=order.order_sum,
                description=f"فاکتور شما # {order.id}",
                is_pay=True
            )
            for detail in order.order_details.all():
                detail.course.user.add(detail.order.user)

            return True
        return False
    except Order.DoesNotExist:
        return False


def use_discount(order, discount_code):
    try:
        discount = Discount.objects.get(discount_code=discount_code)

        if discount.start_date is not None and discount.start_date < datetime.now():
            return DiscountUseType.ExpiredDate.name

        if discount.end_date is not None and discount.end_date > datetime.now():
            return DiscountUseType.ExpiredDate.name

        if discount.usable_count is not None and discount.usable_count < 1:
            return DiscountUseType.Finished.name

        if UserDiscountCode.objects.filter(Q(user=order.user) & Q(discount=discount)).exists():
            return DiscountUseType.UserUsed.name

        order.order_sum = order.order_sum - (order.order_sum * discount.discount_percent/100)
        order.save()

        if discount.usable_count is not None:
            discount.usable_count -= 1
            discount.save()
        UserDiscountCode.objects.create(
            user=order.user,
            discount=discount
        )
        return DiscountUseType.Success.name
    except Discount.DoesNotExist:
        return DiscountUseType.NotFound.name
