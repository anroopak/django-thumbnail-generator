import os

from  django.conf import settings

_MB_TO_BYTES = 1024 * 1024
_settings = getattr(settings, 'CUSTOM_SETTINGS', {})


class AmuzeConfig(object):
    ALL = _settings

    MAX_STR_LENGTH = _settings.get('MAX_STR_LENGTH', 255)
    SUPPORTED_FORMATS = _settings.get('SUPPORTED_FORMATS', ['video/mp4'])
    SUPPORTED_FILE_SIZE = _settings.get("MAX_FILE_SIZE_IN_MB", 2) * _MB_TO_BYTES

    TMP_FOLDER = _settings.get('TMP_FOLDER', "./tmp")
    MEDIA_FOLDER = _settings.get('MEDIA_FOLDER', "./media")
    MEDIA_URL = settings.MEDIA_URL
    THUMBNAIL_FOLDER = _settings.get('THUMBNAIL_FOLDER', "./thumbnail")

    THUMBNAIL_WIDTH = _settings.get("THUMBNAIL_WIDTH", 640)
    THUMBNAIL_HEIGHT = _settings.get("THUMBNAIL_HEIGHT", 320)

    if not os.path.exists(TMP_FOLDER):
        os.mkdir(TMP_FOLDER)
    if not os.path.exists(MEDIA_FOLDER):
        os.mkdir(MEDIA_FOLDER)
    if not os.path.exists(THUMBNAIL_FOLDER):
        os.mkdir(THUMBNAIL_FOLDER)
