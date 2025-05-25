import time
import dns.resolver

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType


class dns_lookup(Heuristic):

    dns_record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SRV', 'SOA', 'TXT', 'CAA', 
    'DS', 'DNSKEY', 'AFSDB', 'APL', 'CDNSKEY', 'CDS', 'CERT', 'CSYNC', 'DHCID', 'DLV']

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def email(query: str):
        pass #TODO: ABUSE NCSC

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        # Simulate fetching data
        for rdata in dns.resolver.query(query, 'ANY'):
            print(rdata)

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        raise NotImplementedError(
            "This is a test heuristic and does not implement "
            "allowed_query_types.")
