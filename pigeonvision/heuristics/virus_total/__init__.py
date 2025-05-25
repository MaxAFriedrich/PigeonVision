import logging
import os
import time
import math

import dotenv
import requests

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType
from pigeonvision.validate.utils import extract_domain


class virus_total(Heuristic):
    logger = logging.getLogger(__name__)

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch_query(query: str, query_type: QueryType, url: str) -> Result:
        response = requests.get(url, headers=virus_total.headers)
        response.raise_for_status()
        data = response.json().get("data", {}).get("attributes", {})
        summary = data.get("last_analysis_stats", {})
        total = summary.get("undetected", 0) + \
                summary.get("malicious", 0) + summary.get("suspicious", 0) + \
                summary.get("harmless", 0)
        malicious = summary.get("malicious", 0) + summary.get("suspicious", 0)
        if total == 0:
            return Result(
                certainty=-1,
                message="<h2>VirusTotal</h2>VirusTotal has no data, and so has been disregarded",
                raw=data,
                timestamp=time.time()
            )
        elif total == 0:
            certainty = 0
        else:
            certainty = 1 - 1/math.exp(12.5*(malicious / total))

        virus_total.logger.debug(
            f"Got certainty of {certainty} for {query} of type {query_type}")

        html = (f"<h2>VirusTotal {query_type.value.capitalize()} Analysis</h2>"
                f"<p>Of {total} antivirus products, {malicious} said the "
                f"{query_type.value.lower()} "
                f"was malicious or suspicious. ")
        if malicious > 0:
            virus_total.logger.debug(
                f"There is at least one detection for {query}")
            engines = data.get("last_analysis_results", {})
            html += (
                f"<p>The following antivirus products flagged the "
                f"{query_type.value.lower()} as "
                "malicious or suspicious:<ul>")
            for engine, result in engines.items():
                if result.get("category") in ["malicious", "suspicious"]:
                    html += (f"<li>{engine}: "
                             f"{result.get('result', 'No result')}</li>")
            html += "</ul>"

        return Result(
            certainty=certainty,
            message=html,
            raw=data,
            timestamp=time.time()
        )

    @staticmethod
    def file(query: str, query_type: QueryType) -> Result:
        url = f"https://www.virustotal.com/api/v3/files/{query}"
        try:
            virus_total.logger.debug(
                f"Fetching VirusTotal data for file {query} of type "
                f"{query_type}")
            return virus_total.fetch_query(query, query_type, url)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                virus_total.logger.warning(
                    f"File {query} not found in VirusTotal.")
                return Result(
                    certainty=-1,
                    message=f"<h2>VirusTotal Error</h2><p>VirusTotal does not "
                            f"know about this file, if it is not "
                            f"confidential, you may wish to upload it "
                            f"yourself.</p>",
                    raw={},
                    timestamp=time.time()
                )
            raise e

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        virus_total.logger.info(
            f"Starting VirusTotal heuristic for {query} of type {query_type}")
        dotenv.load_dotenv()
        virus_total.headers = {
            "accept": "application/json",
            "x-apikey": os.environ.get("VIRUSTOTAL_API_KEY")
        }
        if not virus_total.headers["x-apikey"]:
            raise ValueError(
                "VIRUSTOTAL_API_KEY environment variable is not set.")
        if query_type == QueryType.MD5 or query_type == QueryType.SHA1:
            return virus_total.file(query, query_type)
        if query_type in [QueryType.URL, QueryType.EMAIL]:
            query = extract_domain(query)
            virus_total.logger.debug(
                f"Fetching VirusTotal data for domain {query}")
            url = f"https://www.virustotal.com/api/v3/domains/{query}"
            return virus_total.fetch_query(query, query_type, url)
        if query_type in [QueryType.IPv4, QueryType.IPv6]:
            virus_total.logger.debug(
                f"Fetching VirusTotal data for IP address {query}")
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{query}"
            return virus_total.fetch_query(query, query_type, url)
        if query_type == QueryType.DOMAIN:
            virus_total.logger.debug(
                f"Fetching VirusTotal data for domain {query}")
            url = f"https://www.virustotal.com/api/v3/domains/{query}"
            return virus_total.fetch_query(query, query_type, url)

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.MD5, QueryType.SHA1,
                QueryType.IPv4, QueryType.IPv6, QueryType.DOMAIN,
                QueryType.EMAIL]


if __name__ == "__main__":
    heuristic = virus_total(
        "1.1.1.1",
        QueryType.IPv4)
    heuristic.run(force_fetch=True)
    print(heuristic.result)
