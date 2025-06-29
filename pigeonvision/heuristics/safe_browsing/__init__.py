import time

import dotenv
import requests

from pigeonvision.heuristics.base import Heuristic, Result
from pigeonvision.validate import QueryType


class safe_browsing(Heuristic):

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        dotenv.load_dotenv()
        data = {
            "client": {
                "clientId": "PigeonVision",
                "clientVersion": "1.5.2"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING",
                                "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": query},
                ]
            }
        }
        api_key = dotenv.get_key(dotenv.find_dotenv(), "SAFE_BROWSING_API_KEY")
        url = (f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key"
               f"={api_key}")
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=data)
        matches = response.json().get("matches", [])
        if len(matches) > 0:
            is_flagged = True
            certainty = 0.95
        else:
            is_flagged = False
            certainty = -1
        html = (
            "<h2>Google Safe Browsing</h2>"
            f"<p>This URL is {'not ' if not is_flagged else ''}flagged as "
            f"malicious by Google Safe "
            "Browsing. Google Safe Browsing is a service that "
            "identifies unsafe web resources and provides lists of "
            "malicious URLs to help protect users from phishing, "
            "malware, and unwanted software.</p>"
            "</p>")
        return Result(
            certainty=certainty,
            message=html,
            raw=matches,
        )

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.URL, QueryType.DOMAIN]


if __name__ == '__main__':
    heuristic = safe_browsing(
        "http://malware.tesing/malware/", QueryType.URL)
    print(heuristic.result)
