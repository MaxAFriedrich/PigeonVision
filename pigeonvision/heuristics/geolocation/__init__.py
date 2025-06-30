import logging
import os

import requests
from dotenv import load_dotenv

from pigeonvision.heuristics.base import Heuristic, Result
from pigeonvision.validate import QueryType
from pigeonvision.validate.utils import extract_domain


class geolocation(Heuristic):
    logger = logging.getLogger(__name__)

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        # curl ipinfo.io/{query}?token={IPINFO_KEY}
        # {
        #     "ip": "8.8.8.8",
        #     "hostname": "dns.google",
        #     "city": "Mountain View",
        #     "region": "California",
        #     "country": "US",
        #     "loc": "37.4056,-122.0775",
        #     "org": "AS15169 Google LLC",
        #     "postal": "94043",
        #     "timezone": "America/Los_Angeles",
        #     "anycast": true
        # }
        geolocation.logger.debug("Starting geolocation")

        if query_type == QueryType.URL:
            query = extract_domain(query)
            geolocation.logger.debug(
                f"Extracted domain from URL: {query}, running geolocation on "
                f"it as {query}")
        load_dotenv()
        res = requests.get(f'https://ipinfo.io/{query}',
                           params={'token': os.environ['IPINFO_KEY']})
        if res.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch geolocation data for {query}: {res.text}")
        data = res.json()
        if data.get('error'):
            raise RuntimeError(
                f"Geolocation query failed for {query}: {res.text}")
        geolocation.logger.debug(
            f"Geolocation data fetched successfully for {query}")
        loc = data.get('loc', '0.0,0.0').split(',')
        lat = float(loc[0]) if len(loc) > 0 else 0.0
        lon = float(loc[1]) if len(loc) > 1 else 0.0
        html = (
            "<h2>Geolocation Information</h2>"
            f"<p>Looks to be located in {data.get('city', 'unknown')}, "
            f"{data.get('region', 'unknown')}, "
            f"{data.get('country', 'unknown')}.</p>"
            "<p>This is not factored into the confidence score as geolcation "
            "is not be reliable.</p>"
            f'<iframe width="100%" height="400" frameborder="0" '
            f'scrolling="no" src="https://www.openstreetmap.org/export/embed'
            f'.html?bbox={lon - 0.5}%2C{lat - 0.5}%2C{lon + 0.5}%2C'
            f'{lat + 0.5}&layer=mapnik&marker={lat}%2C{lon}" '
            f'style="border:0;"></iframe>'

        )
        return Result(
            raw=data,
            certainty=-1,
            message=html
        )

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.IPv6, QueryType.IPv4, QueryType.DOMAIN, QueryType.URL]


if __name__ == '__main__':
    location = geolocation('1.1.1.1', QueryType.IPv4)
    print(location.result)
