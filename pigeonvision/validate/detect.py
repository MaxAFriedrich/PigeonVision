from pigeonvision.validate import QueryType


# TODO - Implement additional checks for other query types like MD5, SHA1, etc.

def detect(query: str) -> QueryType:
    for check in [is_url]:
        result = check(query)
        if result:
            return result

    return QueryType.UNKNOWN
