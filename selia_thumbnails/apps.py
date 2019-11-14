import glob
import os
import importlib

from django.apps import AppConfig


class SeliaThumbnailsConfig(AppConfig):
    name = 'selia_thumbnails'

    def ready(self):
        modules = glob.glob(os.path.join(
            os.path.dirname(__file__),
            'processors',
            '*.py'))

        for module in modules:
            if '__init__' in module:
                continue

            filename = os.path.basename(module)
            name, _ = os.path.splitext(filename)

            module_path = '{app}.processors.{name}'.format(
                app=self.name,
                name=name)
            importlib.import_module(module_path)
