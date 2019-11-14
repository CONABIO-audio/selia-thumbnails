from django.urls import path
from selia_thumbnails.views import upload
from selia_thumbnails.views import generate_thumbnail


urlpatterns = [
    path('', upload, name="item_upload"),
    path('thumbnails', generate_thumbnail, name="thumbnails"),
]
