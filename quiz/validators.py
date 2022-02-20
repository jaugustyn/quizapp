from django.core.exceptions import ValidationError
import os


def validate_img_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path & filename
    valid_extensions = ['.apng', '.avif', '.gif', '.jpg', 'jpeg', '.png', '.svg', '.webp', '.bmp', '.ico', '.cur', '.tif', '.tiff']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
