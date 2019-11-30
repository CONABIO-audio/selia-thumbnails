from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.shortcuts import redirect
from sorl.thumbnail import get_thumbnail

from irekua_database.models import Item
from irekua_permissions.items import items as permissions


@require_GET
def generate_thumbnail(request):
    item = Item.objects.get(pk=request.GET["pk"])
    geometry = '100x100'

    if 'size' in request.GET:
        geometry = request.GET["size"]
    elif 'width' in request.GET:
        geometry = request.GET['width']
    elif 'height' in request.GET:
        geometry = request.GET['height']

    crop = request.GET.get("crop", 'center')
    upscale = request.GET.get("upscale", True)
    quality = request.GET.get("quality", 95)
    progressive = request.GET.get("progressive", True)
    orientation = request.GET.get("orientation", True)
    format = request.GET.get("format", 'JPEG')
    colorspace = request.GET.get("colorspace", 'RGB')
    padding = request.GET.get("padding", True)
    padding_color = request.GET.get("padding_color", '#ffffff')

    try:
        image = get_thumbnail(
            item.item_thumbnail,
            geometry,
            crop=crop,
            quality=quality,
            upscale=upscale,
            progressive=progressive,
            orientation=orientation,
            format=format,
            colorspace=colorspace,
            padding=padding,
            padding_color=padding_color)
    except Exception as error:
        print(error)
        return HttpResponse(status=500)

    return redirect(image.url)


def no_permission_redirect():
    return None
