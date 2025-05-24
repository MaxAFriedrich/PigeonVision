import time
import dns.resolver

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType


class dns_lookup(Heuristic):

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        # Simulate fetching data
        for rdata in dns.resolver.query(query, 'CNAME'):
            print(rdata)

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        raise NotImplementedError(
            "This is a test heuristic and does not implement "
            "allowed_query_types.")
