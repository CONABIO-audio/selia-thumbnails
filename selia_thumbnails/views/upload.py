from django.http import JsonResponse
from django.shortcuts import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.forms import ModelForm
from django.db.utils import IntegrityError

from irekua_database.models import Item
from selia_thumbnails.thumbnails import create_thumbnail


class UploadForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            "item_type",
            "item_file",
            "sampling_event_device",
            "source",
            "captured_on",
            "captured_on_year",
            "captured_on_month",
            "captured_on_day",
            "captured_on_hour",
            "captured_on_minute",
            "captured_on_second",
            "captured_on_timezone",
            "licence",
            "tags"
        ]


@require_POST
def upload(request):
    form = UploadForm(request.POST, request.FILES)

    if form.is_valid():
        print('valid form')
        return process_valid_form(request, form)

    return JsonResponse({"result_type": "invalid_form", "result": form.errors}, status=400)


def process_valid_form(request, form):
    item = form.save(commit=False)
    item.created_by = request.user

    try:
        item.save()
    except (ValidationError, IntegrityError) as error:
        return handle_validation_error(item, error)
    except Exception as error:
        return handle_unknown_error(error)

    return handle_succesful_save(item)


def get_item_detail_url(pk):
    try:
        ITEM_DETAIL_APP = settings.ITEM_DETAIL_APP
        detail_view = '{}:item_detail'.format(ITEM_DETAIL_APP)
    except AttributeError:
        detail_view = None

    if detail_view is None:
        return ''

    return reverse(detail_view, args=[pk])


def handle_succesful_save(item):
    create_thumbnail(item)

    upload_result = {
        "result_type": "success",
        "result": {
            "item": {
                "pk": item.pk,
                "detail_url": get_item_detail_url(item.pk),
                "url": item.item_file.url
            }
        }
    }
    return JsonResponse(upload_result, status=200)



def handle_validation_error(item, error):
    if isinstance(error, IntegrityError) or 'hash' in error.message_dict:
        duplicate = Item.objects.get(hash=item.hash)

        upload_result = {
            "result_type": "duplicate",
            "result": {
                "item": {
                    "pk": duplicate.pk,
                    "detail_url": get_item_detail_url(duplicate.pk),
                    "url": duplicate.item_file.url
                }
            }
        }
        return JsonResponse(upload_result, status=400)

    return handle_unknown_error(error)


def handle_unknown_error(error):
    return JsonResponse({"result_type": "unknown", "result": str(error)}, status=400)
