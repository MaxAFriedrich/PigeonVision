from pigeonvision.validate import whitelist
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
        is_whitelisted = whitelist.url(query)
    elif query_type == QueryType.DOMAIN:
        is_whitelisted = whitelist.domain(query)
    elif query_type == QueryType.IPv4 or query_type == QueryType.IPv6:
        is_whitelisted = whitelist.ip(query)
    elif query_type == QueryType.EMAIL:
        is_whitelisted = whitelist.email(query)
    elif query_type in [QueryType.MD5, QueryType.SHA1]:
        is_whitelisted = whitelist.hash(query)

    return (
        query_type,
        ValidationOutcome.WHITELIST if is_whitelisted else
        ValidationOutcome.UNCERTAIN,
        query
    )
