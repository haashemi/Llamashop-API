from urllib.parse import unquote_plus, quote_plus
from string import hexdigits
from hashlib import sha3_512
from random import choice


def quote_string(text):
    return quote_plus(text)


def unquote_string(text):
    return unquote_plus(text)


def get_random_password():
    return ''.join(choice(hexdigits) for _ in range(12))


def hash_string(text: str):
    return sha3_512(bytes(text, 'utf-8')).hexdigest()
