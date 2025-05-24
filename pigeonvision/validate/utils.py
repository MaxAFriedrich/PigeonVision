from __future__ import annotations

from enum import Enum


class ValidationOutcome(Enum):
    WHITELIST = "whitelist"
    INVALID = "invalid"
    UNCERTAIN = "uncertain"


class QueryType(Enum):
    MD5 = "md5"
    SHA1 = "sha1"
    URL = "url"
    DOMAIN = "domain"
    IPv4 = "ipv4"
    IPv6 = "ipv6"
    EMAIL = "email"
    UNKNOWN = "unknown"

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

def extract_domain(query: str) -> str:
    """
    Extracts the domain from a URL or query string.

    :param query: The query string to extract the domain from.
    :return: The extracted domain or an empty string if not found.
    """
    import re
    match = re.search(r'^(?:https?://)?(?:www\.)?([^/]+)', query)
    return match.group(1) if match else ''
