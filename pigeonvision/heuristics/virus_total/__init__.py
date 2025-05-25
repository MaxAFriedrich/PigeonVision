import base64
import logging
import os
import time

import dotenv
import requests

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType


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
        if malicious == 0 or total == 0:
            certainty = 0.0
        else:
            certainty = malicious / total

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
    def url(query: str) -> Result:
        url = "https://www.virustotal.com/api/v3/urls"
        response = requests.post(url, headers=virus_total.headers, data={
            "url": query
        })
        response.raise_for_status()
        virus_total.logger.info(f"URL submitted to VirusTotal: {query}")
        b64_query = base64.b64encode(query.encode()).decode()
        url = f"https://www.virustotal.com/api/v3/urls/{b64_query}"
        for i in [0.1, 5]:
            time.sleep(i)
            try:
                virus_total.logger.debug(
                    f"Fetching VirusTotal data for URL {query} with b64 query "
                    f"{b64_query}")
                return virus_total.fetch_query(b64_query, QueryType.URL, url)
            except requests.HTTPError as e:
                if e.response.status_code != 404:
                    raise e
        return Result(
            certainty=-1,
            message=f"<h2>VirusTotal Error</h2><p>VirusTotal does not "
                    f"know about this URL, if it is not confidential, you "
                    f"may wish to upload it yourself. We did try to upload "
                    f"it, but they did not have the results in time.</p>",
            raw={},
            timestamp=time.time()
        )

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
        if query_type == QueryType.URL:
            return virus_total.url(query)
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
                QueryType.IPv4, QueryType.IPv6, QueryType.DOMAIN]


if __name__ == "__main__":
    heuristic = virus_total(
        "1.1.1.1",
        QueryType.IPv4)
    heuristic.run(force_fetch=True)
    print(heuristic.result)
