import ipaddress

from pigeonvision.validate.utils import extract_domain


# TODO whitelist prvate and reserved IPs

def url(query: str) -> bool:
    # TODO - Implement a proper URL whitelist check
    if query == "https://google.com":
        return True

    return domain(extract_domain(query))


def domain(query: str) -> bool:
    # TODO - Implement a proper domain whitelist check
    if query == "google.com":
        return True

    return False


def is_reserved_ip(query: str) -> bool:
    try:
        ip_ = ipaddress.ip_address(query.strip())
        return (
                ip_.is_private or
                ip_.is_loopback or
                ip_.is_link_local or
                ip_.is_multicast or
                ip_.is_reserved or
                ip_.is_unspecified
        )
    except ValueError:
        return False


def ip(query: str) -> bool:
    if is_reserved_ip(query):
        return True
    # TODO add a proper IP whitelist check
    return False


def email(query: str) -> bool:
    # TODO - Implement a proper email whitelist check
    return domain(extract_domain(query))


def hash(query: str) -> bool:
    # TODO - Implement a proper hash whitelist check
    return False
