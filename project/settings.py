from irekua_dev_settings.settings import *
from irekua_database.settings import *
from selia_thumbnails.settings import *


INSTALLED_APPS = (
    SELIA_THUMBNAILS_APPS +
    IREKUA_DATABASE_APPS +
    IREKUA_BASE_APPS
)
