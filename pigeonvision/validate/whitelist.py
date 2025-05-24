from pigeonvision.validate.utils import extract_domain


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


def ip(query: str) -> bool:
    # TODO - Implement a proper IP whitelist check
    return None


def email(query: str) -> bool:
    # TODO - Implement a proper email whitelist check
    return None


def hash(query: str) -> bool:
    # TODO - Implement a proper hash whitelist check
    return None
