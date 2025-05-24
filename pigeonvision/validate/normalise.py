def domain(query: str) -> str:
    return query.lower().strip()


def url(query: str) -> str:
    if query.startswith('http://'):
        query = query[7:]
    if query.startswith('https://'):
        query = query[8:]
    dot_split = query.split('.')
    if len(dot_split) < 2:
        return query.strip()
