from pigeonvision.validate import whitelist, normalise
from pigeonvision.validate.detect import detect
from pigeonvision.validate.utils import QueryType, ValidationOutcome

__ALL__ = [QueryType, ValidationOutcome]


def validate_query(query: str) -> (QueryType, ValidationOutcome, str):
    if not query:
        return QueryType.UNKNOWN, ValidationOutcome.INVALID, query
    if len(query) < 3:
        return QueryType.UNKNOWN, ValidationOutcome.INVALID, query

    query_type = detect(query)
    if query_type == QueryType.UNKNOWN:
        return QueryType.UNKNOWN, ValidationOutcome.INVALID, query

    is_whitelisted = False
    if query_type == QueryType.URL:
        query = normalise.url(query)
        is_whitelisted = whitelist.url(query)
    elif query_type == QueryType.DOMAIN:
        query = normalise.domain(query)
        is_whitelisted = whitelist.domain(query)
    elif query_type == QueryType.IPv4 or query_type == QueryType.IPv6:
        query = normalise.ip(query)
        is_whitelisted = whitelist.ip(query)
    elif query_type == QueryType.EMAIL:
        query = normalise.email(query)
        is_whitelisted = whitelist.email(query)
    elif query_type in [QueryType.MD5, QueryType.SHA1]:
        query = normalise.hash(query)
        is_whitelisted = whitelist.hash(query)

    return (
        query_type,
        ValidationOutcome.WHITELIST if is_whitelisted else
        ValidationOutcome.UNCERTAIN,
        query
    )


if __name__ == "__main__":
    assert validate_query("https://google.com") == (
        QueryType.URL,
        ValidationOutcome.WHITELIST,
        "google.com"
    )
    assert validate_query("google.com") == (
        QueryType.DOMAIN,
        ValidationOutcome.WHITELIST,
        "google.com"
    )
    assert validate_query("adfjkhlkdsjahf") == (
        QueryType.UNKNOWN,
        ValidationOutcome.INVALID,
        "adfjkhlkdsjahf"
    )
    assert validate_query("1.1.1.1") == (
        QueryType.IPv4,
        ValidationOutcome.WHITELIST,
        "1.1.1.1"
    )
    assert validate_query("2001:0db8:85a3:0000:0000:8a2e:0370:7334") == (
        QueryType.IPv6,
        ValidationOutcome.UNCERTAIN,
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
