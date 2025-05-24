from __future__ import annotations

from enum import Enum


class QueryType(Enum):
    MD5 = "md5"
    SHA1 = "sha1"
    URL = "url"
    DOMAIN = "domain"
    IPv4 = "ipv4"
    IPv6 = "ipv6"
    EMAIL = "email"

    def __dict__(self):
        return {
            'name': self.name,
            'value': self.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> QueryType:
        """
        Converts a dictionary to a QueryType enum.

        :param data: Dictionary containing 'name' and 'value' keys.
        :return: Corresponding QueryType enum.
        """
        return cls(data['value']) if 'value' in data else cls(data['name'])
