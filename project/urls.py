from django.conf.urls import url
from django.conf.urls import include


urlpatterns = [
    url(
        r'processes/thumbnails/',
        include(('selia_thumbnails.urls', 'selia_thumbnails'))),
]
