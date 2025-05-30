import time
import dns.resolver
import logging
import requests

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType
from pigeonvision.validate.utils import extract_domain


class dns_lookup(Heuristic):

    dns_record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SRV', 'SOA', 'TXT', 'CAA',
    'DS', 'DNSKEY', 'AFSDB', 'APL', 'CDNSKEY', 'CDS', 'CERT', 'CSYNC', 'DHCID', 'DLV']

    logger = logging.getLogger(__name__)

    email_endpoints = [('DMARC', 'https://scan.emailsecuritycheck.service.ncsc.gov.uk/dmarc/', 'This domain has a strong DMARC policy in place'),
                        ('SPF', 'https://scan.emailsecuritycheck.service.ncsc.gov.uk/spf/', 'We did not detect any issues with your SPF record'),
                        ('TLS', 'https://scan.emailsecuritycheck.service.ncsc.gov.uk/tls/', 'No issues found with the TLS configuration'),
                        ('MTASTS', 'https://scan.emailsecuritycheck.service.ncsc.gov.uk/mtasts/', 'Privacy of emails to this domain is protected from downgrade attacks')]

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def email(query: str) -> (float, str):

        base_good = 0

        msg = ''

        for test, endpoint, expected in dns_lookup.email_endpoints:
            res = requests.get(endpoint + query)

            if res.json()['summary']['title'] != expected:
                if test == 'SPF': base_good += 0.4
                else: base_good += 0.2

            print(f"{test} resulted in {res.json()['summary']['title']}")

        return (base_good, msg)

    @staticmethod
    def fetch(query: str, query_type: QueryType):

        query = extract_domain(query)

        dns_lookup.logger.info("Starting DNS and email queries for %s", query)

        results = {}

        email_confidence = -1

        for record in dns_lookup.dns_record_types:
            dns_lookup.logger.debug("Querying %s record", record)
            records = []

            try:
                for rdata in dns.resolver.query(query, record):
                    records.append(str(rdata))
            except dns.resolver.NoAnswer as e:
                dns_lookup.logger.debug("%s record not found", record)
                continue
            if records != []: results[record] = records

        if 'MX' in results or query_type == QueryType.EMAIL:
            msg = ("<h2> DNS and email </h2> We checked the email records for this domain"
                " and checked for records that suggest email is properly set up."
                " It's often not a huge deal if they aren't, but it does indicate that "
                "something is up.<br><br>")
            email_confidence, email_msg = dns_lookup.email(query)

            msg += email_msg
            msg += f"Based on the above, we gave the email a malicious confidence of {email_confidence} <br><br>"


        else:
            msg = '<h2> DNS </h2>'

        msg += "Below are the DNS records found on this domain<br><br>"
        msg += '<table class="dns-table">'
        msg += '<tr><th>Field</th><th>Value</th></tr>'

        for key in results:

            msg += (
                f'<tr><td>{key}</td><td>'
                f'{results[key]}</td>')

        msg += '</table>'

        return Result(
                certainty=email_confidence,
                raw=results,
                message=msg)

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.EMAIL, QueryType.DOMAIN, QueryType.URL]
