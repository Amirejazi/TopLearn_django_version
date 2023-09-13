from io import BytesIO
from PIL import Image
import os

from django.db.models import Q

from TopLearn.settings import MEDIA_ROOT


def compact_and_resize_image(image_path, new_width):
    # Open the image
    image = Image.open(image_path)

    # Compress the image
    # compressed_image = BytesIO()

    format = os.path.splitext(str(image_path))[1]
    image.save(os.path.basename(str(image_path)), quality=100)

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
        courses = courses.filter(Q(courseTitle__icontains=search_filter))

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
