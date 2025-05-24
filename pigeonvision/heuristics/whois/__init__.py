import time
import requests
import math

from datetime import date, datetime
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

        date_format = "%Y-%m-%d"

        res = requests.get(f'https://www.whois.com/whois/{query}', params=params)
        whois = {}

        data = BeautifulSoup(res.text, 'html.parser').main

        for div in data.find_all("div", {"class": "df-row"}):

            whois[div.contents[0].text] = div.contents[1].text

        time_since_reg = datetime.now() - datetime.strptime(whois['Registered On:'], date_format)
        if time_since_reg.days > 5000: return Result(
                certainty = -1,
                raw = whois,
                timestamp = time.time(),
                message = str(whois)
                )

        time_to_exp = datetime.strptime(whois['Expires On:'], date_format) - datetime.now()
        normalised = (40 / math.exp(1/4 * time_since_reg.days)) / 100

        if normalised < 0.00001: normalised = -1

        if time_to_exp.days < 2: normalised = 0.4

        return Result(
                certainty = normalised,
                raw = whois,
                timestamp = time.time(),
                message = str(whois)
                )


    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        raise NotImplementedError(
            "This is a test heuristic and does not implement "
            "allowed_query_types.")
