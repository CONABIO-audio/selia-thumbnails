import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

from selia_thumbnails.thumbnails import register_processor


SIZE = (500, 500)


@register_processor('image/png')
@register_processor('image/jpeg')
def image_processor(item):
    image = Image.open(item.item_file)
    tmp = image.convert('RGB')
    tmp.thumbnail(SIZE, Image.ANTIALIAS)
    tmp_io = io.BytesIO()
    tmp.save(fp=tmp_io, format='JPEG')
    im_file = InMemoryUploadedFile(
        tmp_io, None,
        'thumbnail.jpg',
        'image/jpeg',
        tmp_io.getbuffer().nbytes,
        None)
    return im_file
