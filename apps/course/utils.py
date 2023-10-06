import mimetypes
from io import BytesIO
from urllib.parse import quote
from PIL import Image
import os
from django.db.models import Q, Sum, F
from django.http import HttpResponse, HttpResponseNotFound
from TopLearn.settings import MEDIA_ROOT
from django.apps import apps


def compact_and_resize_image(image_path, new_width):
    # Open the image
    image = Image.open(image_path)

    # Compress the image
    # compressed_image = BytesIO()

    format = os.path.splitext(str(image_path))[1]

    # Resize the image
    aspect_ratio = float(image.size[1]) / float(image.size[0])
    new_height = int(aspect_ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    # image.thumbnail((new_width, new_height))
    # Save the resized image
    resized_image_path = MEDIA_ROOT + 'images/course/thumb/' + os.path.basename(os.path.splitext(str(image_path))[0]) + format
    resized_image.save(resized_image_path)

    return resized_image_path


def apply_filters_on_courses(courses, search_filter, get_type, order_by_type, start_price, end_price, group_filter):
    if search_filter:
        courses = courses.filter(Q(courseTitle__icontains=search_filter) | Q(tags__icontains=search_filter))

    if get_type:
        match get_type:
            case "buy":
                courses = courses.filter(~Q(price=0))
            case "free":
                courses = courses.filter(Q(price=0))

    if order_by_type:
        match order_by_type:
            case "date":
                courses = courses.order_by('-createDate')
            case "updatedate":
                courses = courses.order_by('-updateDate')

    if start_price:
        courses = courses.filter(price__gt=start_price)
    if end_price:
        courses = courses.filter(price__lt=end_price)

    if group_filter:
        for groupid in group_filter:
            courses = courses.filter(Q(group__id=groupid) | Q(subGroup__id=groupid))

    return courses


def add_order(user, course):
    Order = apps.get_model('order', 'Order')
    OrderDetail = apps.get_model('order', 'OrderDetail')
    try:
        order = Order.objects.get(Q(user=user) & Q(is_finaly=False))
        try:
            order_detail = OrderDetail.objects.get(Q(order=order) & Q(course=course))
            order_detail.count += 1
            order_detail.save()
        except OrderDetail.DoesNotExist:
            OrderDetail.objects.create(
                order=order,
                course=course,
                count=1,
                price=course.price
            )
        finally:
            order.order_sum = OrderDetail.objects.filter(order=order).aggregate(total=Sum(F('price') * F('count')))['total']
            order.save()
            return order.id
    except Order.DoesNotExist:
        order = Order.objects.create(
            user=user,
            is_finaly=False,
            order_sum=course.price,
        )
        OrderDetail.objects.create(
            order=order,
            course=course,
            count=1,
            price=course.price
        )
        return order.id


def downloadFile(file_path):
    if os.path.exists(file_path):
        file_type = mimetypes.guess_type(file_path)
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=f"application/{file_type}")
            file_name_encoded = quote(os.path.basename(file_path))
            response['Content-Disposition'] = f'attachment; filename={file_name_encoded}'
            return response
    else:
        return HttpResponseNotFound('فایل مورد نظر یافت نشد')