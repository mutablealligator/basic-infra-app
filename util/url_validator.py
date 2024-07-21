import logging

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)
val = URLValidator()
SHORT_CODE_VALID_LENGTH = 8


def is_valid_url(url):
    try:
        val(url)
        return True
    except (ValueError, ValidationError,) as e:
        logger.warning(e)
        return False


def is_valid_short_code(short_code: str) -> bool:
    if (not short_code or
        len(short_code) != SHORT_CODE_VALID_LENGTH or
        not short_code.isalnum()):
        return False
    return True
