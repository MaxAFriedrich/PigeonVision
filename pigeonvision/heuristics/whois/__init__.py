import time
import requests
from bs4 import BeautifulSoup

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType


class whois(Heuristic):

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        # Simulate fetching data
        params = {
            'domain': query,
        }

        res = requests.get(f'https://www.whois.com/whois/{query}', params=params)

        whois = {}

        data = BeautifulSoup(res.text, 'html.parser').main

        for div in data.find_all("div", {"class": "df-row"}):

            whois[div.contents[0].text] = div.contents[1].text

        print(whois)

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        raise NotImplementedError(
            "This is a test heuristic and does not implement "
            "allowed_query_types.")
