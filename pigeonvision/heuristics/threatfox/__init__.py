import json
import os
import time

import dotenv
import requests

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType
from pigeonvision.validate.utils import extract_domain


class threatfox(Heuristic):

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        if query_type == QueryType.EMAIL:
            query = extract_domain(query)

        dotenv.load_dotenv()
        headers = {
            'Auth-Key': os.getenv('THREATFOX_API_KEY', ''),
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {"query": "search_ioc", "search_term": query,
                "exact_match": True}

        response = requests.post('https://threatfox-api.abuse.ch/api/v1/',
                                 headers=headers, data=json.dumps(data))
        response.raise_for_status()

        result = response.json()
        # {'query_status': 'ok', 'data': [{'id': '1534152', 'ioc':
        # 'anefank.mom', 'threat_type': 'botnet_cc', 'threat_type_desc':
        # 'Indicator that identifies a botnet command&control server (C&C)',
        # 'ioc_type': 'domain', 'ioc_type_desc': 'Domain that is used for
        # botnet Command&control (C&C)', 'malware': 'win.sidewinder',
        # 'malware_printable': 'SideWinder', 'malware_alias': None,
        # 'malware_malpedia':
        # 'https://malpedia.caad.fkie.fraunhofer.de/details/win.sidewinder',
        # 'confidence_level': 50, 'first_seen': '2025-05-25 14:42:23 UTC',
        # 'last_seen': None, 'reference': '', 'reporter': 'juroots', 'tags':
        # ['c2', 'SideWinder'], 'malware_samples': []}]}
        if result['query_status'] != 'ok':
            raise ValueError(f"Error fetching data: {result['query_status']}")
        if not result['data']:
            return Result(
                certainty=-1,
                message=f"<h2>ThreatFox</h2><p>No data found for {query}.</p>",
                raw={},
            )
        data = result['data']
        no_results = len(data)
        total = 0
        for res in data:
            total += res.get('confidence_level', 0)
        confidence = total / no_results if no_results > 0 else 0

        message = (
            "<h2>ThreatFox</h2>"
            "<p>ThreatFox is a service that provides information about "
            "malicious indicators of compromise (IoCs) such as domains, "
            "IP addresses, and URLs. It is operated by abuse.ch, a project "
            "that tracks and analyzes cyber threats.</p>"
        )
        if no_results > 0:
            message += (f"<p>It has an overall confidence level of "
                        f"{confidence:.2f}%.</p>")
            message += (
                f"<p>Found {no_results} results for {query}.</p>"
                "<ul>"
            )
            for res in data:
                message += (
                    f"<li><strong>{res.get('ioc_type_desc', 'Unknown Type')}: "
                    f"{res.get('ioc', 'Unknown IOC')}</strong> - "
                    f"Threat Type: {res.get('threat_type_desc', 'Unknown')} "
                    f"({res.get('threat_type', 'Unknown')})<br>"
                    f"Confidence Level: {res.get('confidence_level', 0)}%<br>"
                    f"First Seen: {res.get('first_seen', 'Unknown')}<br>"
                    f"Malware: {res.get('malware_printable', 'Unknown')} "
                    f"({res.get('malware', 'Unknown')})</li>"
                )
            message += "</ul>"
        else:
            message += f"<p>No results were found for {query}.</p>"

        return Result(
            certainty=confidence / 100,
            message=message,
            raw=result,
        )

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [
            QueryType.URL, QueryType.DOMAIN, QueryType.IPv4, QueryType.IPv6,
            QueryType.EMAIL, QueryType.MD5, QueryType.SHA1, QueryType.SHA256
        ]


if __name__ == "__main__":
    heuristic = threatfox(
        "anefank.mom",
        QueryType.IPv4
    )
    print(heuristic.result)
