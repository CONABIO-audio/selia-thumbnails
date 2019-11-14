import mimetypes


mimetypes.init()
MIME_TYPES = set(mimetypes.types_map.values())
THUMBNAIL_PROCESSORS = {}


def register_processor(mime_type):
    if mime_type not in MIME_TYPES:
        raise ValueError('This ({}) mime type is not recognized'.format(mime_type))

    def decorator(func):
        THUMBNAIL_PROCESSORS[mime_type] = func
        return func
    return decorator


def get_processor(mime_type):
    if mime_type not in THUMBNAIL_PROCESSORS:
        raise ValueError('No processor for mime type {} was found'.format(mime_type))

    return THUMBNAIL_PROCESSORS[mime_type]


def create_thumbnail(item):
    mime_type, _ = mimetypes.guess_type(item.item_file.url)
    processor = get_processor(mime_type)
    thumbnail = processor(item)
    item.item_thumbnail = thumbnail
    item.save()
