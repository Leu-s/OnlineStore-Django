from datetime import datetime
from os.path import splitext
from uuslug import slugify
from transliterate import translit
from transliterate import exceptions
import random


def get_timestamp_path(instance, filename):
    return f'{datetime.now().timestamp()}{splitext(filename)[1]}'


def my_slugify(content):
    try:
        content = translit(content, reversed=True)
    except exceptions.LanguageDetectionError:
        pass
    slug = slugify(content)
    return f'{slug}-{random.randint(0, 10000)}'
