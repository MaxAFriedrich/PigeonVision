import time
import os
import logging
import requests

from dotenv import load_dotenv

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType


class urlhaus(Heuristic):

    logger = logging.getLogger(__name__)

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):

        load_dotenv()

        urlhaus.logger.debug("Starting URLHaus")

        msg = "<h2>URLHaus</h2>URLHaus is a service that collects malicious URLs and downloads payloads from them."

        headers = {
            'Auth-Key': os.environ['URLHAUS_KEY']
        }

        if query_type == query_type.DOMAIN or query_type == query_type.IPv4 or \
            query_type == query_type.IPv6 or query_type == query_type.URL:

            msg += "<br><br>We've checked your URL against URLHaus data"

            urlhaus.logger.debug("Getting URL data")
            data = {
                'url': query
            }

            res = requests.post('https://urlhaus-api.abuse.ch/v1/url/', data=data, headers=headers)

            if res.json()['threat'] == 'malware_download':
                msg += ("<br><br>URLHaus indicated that there's malware on the link you've submitted. "
                        "Because of this, the URLHaus score is 1")
                certainty = 1
            elif res.json['query_status'] == 'no_results':
                certainty = -1
            else:
                certainty = 0

            return Result(
                certainty=certainty,
                message=msg,
                raw=res.json(),
                timestamp=time.time()
            )

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.IPv4, QueryType.IPv6, QueryType.DOMAIN, QueryType.URL]
