from enum import Enum


class QueryType(Enum):
    MD5 = "md5"
    SHA1 = "sha1"
    URL = "url"
    DOMAIN = "domain"
    IPv4 = "ipv4"
    IPv6 = "ipv6"
    EMAIL = "email"




