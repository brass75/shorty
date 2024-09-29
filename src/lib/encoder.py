import base64
from hashlib import shake_128 as hash_method


def encode_string(s: str) -> str:
    """
    Compute the hash of the string and return the base64 encoding without trailing =

    :param s: string to encode
    :return: encoded string
    """
    csum = hash_method(s.encode('utf-8'))
    csum = int(csum.hexdigest(8), 16)
    encoded = base64.b64encode(csum.to_bytes(8), b'_-').decode().rstrip('=')
    return encoded
