import os
from urllib.parse import urlparse
import re
import logging

logger = logging.getLogger('utils')

URL_PATTERN = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE,
)


def get_url_prefix(url: str) -> str:
    """
    Return the URL prefix. For example, if the url:
        https://github.com/itsthejoker/spiderweb/blob/main/spiderweb/request.py
    is given it will return:
        https://githum.com

    :param url: to get the prefix for
    :return: The URL prefix
    """
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}' if (parsed.scheme and parsed.netloc) else ''


def validate_url(url: str) -> bool:
    """
    Validates that the string we are being asked to shorten is a valid URL

    :param url: URL to validate
    :return: If it passes muster
    """
    return url is not None and URL_PATTERN.search(url)


def get_data_dir() -> str:
    """
    Dynamically figure out the path to the data directory

    :return: path to the data directory
    """
    curr_dir = os.getcwd()
    logger.warning(f'{curr_dir=}')
    if curr_dir.endswith('/src'):
        curr_dir = curr_dir.removesuffix('/src')
    return os.path.join(curr_dir, 'data')
