from io import BytesIO
from PIL import Image
import os
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