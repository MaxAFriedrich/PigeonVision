import time
import dns.resolver
import logging

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType


class dns_lookup(Heuristic):

    dns_record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SRV', 'SOA', 'TXT', 'CAA', 
    'DS', 'DNSKEY', 'AFSDB', 'APL', 'CDNSKEY', 'CDS', 'CERT', 'CSYNC', 'DHCID', 'DLV']

    logger = logging.getLogger(__name__)

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def email(query: str):
        pass #TODO: ABUSE NCSC

    @staticmethod
    def fetch(query: str, query_type: QueryType):

        dns_lookup.logger.info("Starting DNS and email queries for %s", query)

        results = {}

        for record in dns_lookup.dns_record_types:

            dns_lookup.logger.debug("Querying %s record")
            records = []

            for rdata in dns.resolver.query(query, record):
                records += rdata

            results[record] = records

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        raise NotImplementedError(
            "This is a test heuristic and does not implement "
            "allowed_query_types.")
