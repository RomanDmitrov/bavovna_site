from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile


def compress_image_field(field, quality=90):
    if not field or not isinstance(field.file, UploadedFile):
        return

    image = Image.open(field.file)

    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')

    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=quality, optimize=True)

    field.save(field.name, ContentFile(buffer.getvalue()), save=False)