from hashlib import sha256 as hash_method
import base64


def encode_string(s: str) -> str:
    """
    Compute the hash of the string and return the base64 encoding without trailing =

    :param s: string to encode
    :return: encoded string
    """
    csum = int.from_bytes(hash_method(s.encode()).digest()[:6])
    encoded = base64.b64encode(csum.to_bytes(6)).decode().rstrip('=')
    return encoded
