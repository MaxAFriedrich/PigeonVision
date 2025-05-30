import logging
import math
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType


class whois(Heuristic):
    logger = logging.getLogger(__name__)

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def build_html(result: dict) -> str:
        # result = {'Domain:': 'example.com', 'Registered On:': '1995-08-14',
        #           'Expires On:': '2025-08-13', 'Updated On:': '2024-08-14',
        #           'Status:': 'client delete prohibitedclient transfer '
        #                      'prohibitedclient update prohibited',
        #           'Name Servers:': 'a.iana-servers.netb.iana-servers.net',
        #           'Registrar:': 'RESERVED-Internet Assigned Numbers
        #           Authority',
        #           'IANA ID:': '376', 'Abuse Email:': ''}
        html = ('<h2>Whois Information</h2><p>Whois information for the domain '
                'tells us about the registration and status of the domain.</p>')
        html += '<table class="whois-table">'
        html += '<tr><th>Field</th><th>Value</th><th>Explanation</th></tr>'

        if 'Registered On:' in result:
            html += (
                f'<tr><td>Registered On:</td><td>'
                f'{result["Registered On:"]}</td>'
                f'<td>The date when the domain was registered. Very newly '
                f'registered domains might be suspicious.</td></tr>')

        if 'Expires On:' in result:
            html += (
                f'<tr><td>Expires On:</td><td>{result["Expires On:"]}</td>'
                f'<td>The date when the domain registration expires. If it is '
                f'close to expiration, it might indicate a temporary or '
                f'suspicious domain.</td></tr>')

        if 'Name Servers:' in result:
            html += (
                f'<tr><td>Name Servers:</td><td>{result["Name Servers:"]}</td>'
                f'<td>The name servers associated with the domain. The name '
                f'servers are responsible for resolving the domain to an '
                f'Internet Protocol address. '
                f'Unusual or unrelated name servers can indicate a suspicious '
                f'domain.</td></tr>')

        if 'Registrar:' in result:
            html += (
                f'<tr><td>Registrar:</td><td>{result["Registrar:"]}</td>'
                f'<td>The registrar of the domain. The registrar is the '
                f'organization that the domain was bought through. '
                f'If it is a well-known registrar, '
                f'it is usually a good sign. If it is a suspicious or unknown '
                f'registrar, it might indicate a suspicious domain.</td></tr>')

        html += '</table>'

        return html

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        whois.logger.info("Starting whois heuristic")

        date_format = "%Y-%m-%d"

        res = requests.get(f'https://www.whois.com/whois/{query}')
        whois_data = {}

        data = BeautifulSoup(res.text, 'html.parser').main

        for div in data.find_all("div", {"class": "df-row"}):
            whois_data[div.contents[0].text] = div.contents[1].text
            whois.logger.debug("Parsed out %s : %s", div.contents[0].text,
                               div.contents[1].text)

        registered_on = whois_data.get('Registered On:')
        updated_on = whois_data.get('Updated On:')
        if not registered_on or not updated_on:
            whois.logger.debug(
                f"Could not find registration dates in whois data for {query}")
            return Result(
                certainty=-1,
                raw=whois_data,
                message="<p>Could not find registration dates in whois "
                        "data.</p>"
            )
        time_since_reg = datetime.now() - datetime.strptime(
            registered_on, date_format)
        if time_since_reg.days > 5000:
            return Result(
                certainty=-1,
                raw=whois_data,
                message=whois.build_html(whois_data)
            )

        time_to_exp = datetime.strptime(whois_data['Expires On:'],
                                        date_format) - datetime.now()
        normalised = (40 / math.exp(1 / 4 * time_since_reg.days)) / 100

        if normalised < 0.00001:
            normalised = -1

        if time_to_exp.days < 2:
            normalised = 0.4

        return Result(
            certainty=normalised,
            raw=whois_data,
            message=whois.build_html(whois_data)
        )

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.DOMAIN, QueryType.IPv4, QueryType.IPv6, QueryType.URL]
