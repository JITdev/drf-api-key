"""Cryptographic module for api key handling."""

import typing

from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import get_random_string


def concatenate(left: str, right: str) -> str:
    """Concatenate string parts."""
    return f'{left}.{right}'


def split(concatenated: str) -> typing.Tuple[str, str]:
    """Split concatenated string."""
    left, _, right = concatenated.partition('.')
    return left, right


class KeyGenerator(object):
    """Keygenerator class for api keys."""

    def __init__(self, prefix_length: int = 8, secret_key_length: int = 32):
        """Initialize keygenerator."""
        self.prefix_length = prefix_length
        self.secret_key_length = secret_key_length

    def get_prefix(self) -> str:
        """Get key prefix."""
        return get_random_string(self.prefix_length)

    def get_secret_key(self) -> str:
        """Get secret key."""
        return get_random_string(self.secret_key_length)

    def hash(self, hash_value: str) -> str:
        """Generate hashed string."""
        return make_password(hash_value)

    def generate(self) -> typing.Tuple[str, str, str]:
        """Return key, prefix and hashed key."""
        prefix = self.get_prefix()
        secret_key = self.get_secret_key()
        key = concatenate(prefix, secret_key)
        hashed_key = self.hash(key)
        return key, prefix, hashed_key

    def verify(self, key: str, hashed_key: str) -> bool:
        """Verify key against hashed key."""
        return check_password(key, hashed_key)
