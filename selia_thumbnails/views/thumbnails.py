from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.shortcuts import redirect
from sorl.thumbnail import get_thumbnail

from irekua_database.models import Item
from irekua_permissions.items import items as permissions


@require_GET
def generate_thumbnail(request):
    item = Item.objects.get(pk=request.GET["pk"])
    size = '100x100'
    crop = 'center'
    quality = 99

    if 'size' in request.GET:
        size = request.GET["size"]
    if 'quality' in request.GET:
        quality = int(request.GET["quality"])
    if 'crop' in request.GET:
        crop = request.GET["crop"]

    try:
        image = get_thumbnail(item.item_thumbnail, size, crop=crop, quality=quality)
    except Exception as error:
        return HttpResponse(status=500)

    return redirect(image.url)


def no_permission_redirect():
    return None
