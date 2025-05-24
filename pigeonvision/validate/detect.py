from re import match

import pigeonvision.validate.normalise as normalise
from pigeonvision.validate.tlds import get_tlds
from pigeonvision.validate.utils import extract_domain, QueryType


def ip(query: str) -> QueryType:
    ip_ = normalise.ip(query)
    # ipv4
    if match(r'^\d{1,3}(\.\d{1,3}){3}$', ip_):
        return QueryType.IPv4
    # ipv6
    if match(r'^([0-9a-f]{4}:){7}[0-9a-f]{4}$', ip_):
        return QueryType.IPv6

    return QueryType.UNKNOWN


def email(query: str) -> QueryType:
    # email
    email_ = normalise.email(query)
    last_domain_part = email_.split('@')[-1].split('.')[-1]
    if match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
             email_) and last_domain_part in get_tlds():
        return QueryType.EMAIL
    return QueryType.UNKNOWN


def domain(query: str) -> QueryType:
    # domain
    domain_ = normalise.domain(query)
    if match(r'^[a-zA-Z0-9.-]+(\.[a-zA-Z-0-9]{2,})', domain_) and \
            domain_.split('.')[-1] in get_tlds():
        return QueryType.DOMAIN
    return QueryType.UNKNOWN


def detect(query: str) -> QueryType:
    ip_type = ip(query)
    if ip_type != QueryType.UNKNOWN:
        return ip_type

    email_type = email(query)
    if email_type != QueryType.UNKNOWN:
        return email_type

    domain_type = domain(query)
    if domain_type != QueryType.UNKNOWN:
        return domain_type

    # url
    url = normalise.url(query)
    domain_name = extract_domain(url)
    if (
            match(r'^[a-zA-Z0-9.-]+(:\d+)?(/.*)?$', url) and
            (
                    ip(domain_name) == QueryType.IPv4 or
                    domain(domain_name) == QueryType.DOMAIN
            )
    ):
        return QueryType.URL

    # hash
    hash = normalise.hash(query)
    if match(r'^[a-f0-9]{32}$', hash):
        return QueryType.MD5
    if match(r'^[a-f0-9]{40}$', hash):
        return QueryType.SHA1

    return QueryType.UNKNOWN


if __name__ == '__main__':
    assert detect('http://google.com') == QueryType.URL
    assert detect('https://google.com/foo?bar=baz#meh') == QueryType.URL
    assert detect('google.com') == QueryType.DOMAIN
    assert detect('google.com/foo?bar=baz#meh') == QueryType.URL
    assert detect('http://1.1.1.1/foo?bar=baz#meh') == QueryType.URL
    assert detect('foo:bar@example.com') == QueryType.URL
    assert detect('foo@example.com') == QueryType.EMAIL
    assert detect('http://foo@example.com') == QueryType.URL
    assert detect('5c9814907b996daba3fe0eab5512B452') == QueryType.MD5
    assert detect('7097f3f1fa1eacb10eff04efdf2c4ebab4ca33Ad') == QueryType.SHA1
    assert detect('xn--d1acpjx3f.xn--p1ai') == QueryType.DOMAIN
    assert detect(
        'https://xn--d1acpjx3f.xn--p1ai/path') == QueryType.URL
    assert detect('Google.com \t') == QueryType.DOMAIN
    assert detect('google.com') == QueryType.DOMAIN
    assert detect('https://google.com') == QueryType.URL
    assert detect('http://google.com') == QueryType.URL
    assert (
            detect('http://username:password@google.com/path/to/resource') ==
            QueryType.URL
    )
    assert detect('https://GoOgle.com#fragment') == QueryType.URL
    assert detect('https://google.com?query=param') == QueryType.URL
    assert detect('username@example.com/path') == QueryType.URL
    assert detect('username:password@example.com') == QueryType.URL
    assert (detect(
        'https://www.google.com/path?query=param&foo=bar#attribute') ==
            QueryType.URL)
    assert detect('1.1.1.1   \t') == QueryType.IPv4
    assert detect('2001:0Db8:85A3:0000:0000:8a2e:037:7334') == QueryType.IPv6
    assert detect('2001::2001') == QueryType.IPv6
    assert detect('mailto:exaMple@examplE.com') == QueryType.EMAIL
    assert detect('exaMple@examplE.com') == QueryType.EMAIL
    assert detect('exaMple@examplE.yaysyskjdshfk///') == QueryType.UNKNOWN
    assert detect('exaMple@examplE.com/path') == QueryType.URL
    assert detect('  ExAmpleHash123  ') == QueryType.UNKNOWN
    assert detect('examplle.coom') == QueryType.UNKNOWN
