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

        headers = {
            'Auth-Key': os.environ['URLHAUS_KEY']
        }

        if query_type == query_type.DOMAIN or query_type == query_type.IPv4 or \
            query_type == query_type.IPv6 or query_type == query_type.URL:

            urlhaus.logger.debug("Getting URL data")
            data = {
                'url': query
            }

            res = requests.post('https://urlhaus-api.abuse.ch/v1/payload/', data=data, headers=headers)

            print(res.json())
            return res.json()

        urlhaus.logger.debug("Getting hash data")

        if query_type == QueryType.MD5:
            data = {
                'md5_hash': query
            }

        if query_type == QueryType.SHA256:
            data = {
                'sha256_hash': query
            }

        res = requests.post('https://urlhaus-api.abuse.ch/v1/payload/', data=data, headers=headers)

        return res.json()




        raise NotImplementedError(
            "This is a test heuristic and does not implement fetch.")

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.MD5, QueryType.IPv4, QueryType.IPv6, QueryType.DOMAIN, QueryType.SHA256, QueryType.URL]
