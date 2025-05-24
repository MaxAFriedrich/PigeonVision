import idna


def domain(query: str) -> str:
    # Normalize to lowercase, strip whitespace, and convert to punycode if
    # needed
    query = query.lower().strip()
    try:
        query = idna.encode(query).decode('ascii')
    except idna.IDNAError:
        pass
    return query


def url(query: str) -> str:
    if query.startswith('http://'):
        query = query[7:]
    if query.startswith('https://'):
        query = query[8:]
    dot_split = query.split('.')
    if len(dot_split) < 2:
        return query.strip()
    if "@" in dot_split[0]:
        dot_split[0] = dot_split[0].split('@')[-1]
    if "#" in dot_split[-1]:
        dot_split[-1] = dot_split[-1].split('#')[0]
    if '?' in dot_split[-1]:
        dot_split[-1] = dot_split[-1].split('?')[0]
    path = ''
    if '/' in dot_split[-1]:
        path_split = dot_split[-1].split('/')
        dot_split[-1] = path_split[0]
        path = '/'.join(path_split[1:])
        path = "/" + path.strip()
    domain_ = domain('.'.join(dot_split))
    return domain_ + path


def hash(query: str) -> str:
    return query.strip().lower()


def ip(query: str) -> str:
    if ':' in query:
        # IPv6 address
        query = query.strip().lower()
        parts = query.split(':')
        # Normalize to full notation
        if '' in parts:
            # Handle compressed notation
            empty_index = parts.index('')
            parts = [part.zfill(4) for part in parts if part]
            while len(parts) < 8:
                parts.insert(empty_index, '0000')
        else:
            parts = [part.zfill(4) for part in parts]
        query = ':'.join(parts)
    return query.strip().lower()


def email(query: str) -> str:
    query = query.strip()
    if query.startswith('mailto:'):
        query = query.split('mailto:')[1]
    if '@' in query:
        local_part, domain_part = query.split('@', 1)
        domain_part = domain(domain_part)
        query = f"{local_part}@{domain_part}"
    return query.strip()


if __name__ == '__main__':
    assert domain('xn--d1acpjx3f.xn--p1ai') == 'xn--d1acpjx3f.xn--p1ai'
    assert url(
        'https://xn--d1acpjx3f.xn--p1ai/path') == 'xn--d1acpjx3f.xn--p1ai/path'
    assert domain('Google.com \t') == 'google.com'
    assert url('google.com') == 'google.com'
    assert url('https://google.com') == 'google.com'
    assert url('http://google.com') == 'google.com'
    assert (
            url('http://username:password@google.com/path/to/resource') ==
            'google.com/path/to/resource'
    )
    assert url('https://GoOgle.com#fragment') == 'google.com'
    assert url('https://google.com?query=param') == 'google.com'
    assert url('username@example.com/path') == 'example.com/path'
    assert url('https://example.com:8080/path') == 'example.com:8080/path'
    assert url('username:password@example.com') == 'example.com'
    assert (url(
        'https://www.google.com/path?query=param&foo=bar#attribute') ==
            'www.google.com/path')
    assert ip('1.1.1.1   \t') == '1.1.1.1'
    assert ip('2001:0Db8:85A3:0000:0000:8a2e:0370:7334') == '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
    assert ip('2001::2001') == '2001:0000:0000:0000:0000:0000:0000:2001'
    assert email('mailto:exaMple@examplE.com') == 'exaMple@example.com'
    assert email('exaMple@examplE.com') == 'exaMple@example.com'
    assert email('exaMple@examplE.com/path') == 'exaMple@example.com/path'
    assert hash('  ExAmpleHash123  ') == 'examplehash123'
