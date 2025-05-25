import logging
import time

import requests

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType
from pigeonvision.validate.utils import extract_domain


class geolocation(Heuristic):
    logger = logging.getLogger(__name__)

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        # curl http://ip-api.com/json/24.48.0.1
        # {"status": "success", "country": "Canada", "countryCode": "CA",
        # "region": "QC",
        #  "regionName": "Quebec", "city": "Montreal", "zip": "H1K", "lat":
        #  45.6085,
        #  "lon": -73.5493, "timezone": "America/Toronto",
        #  "isp": "Le Groupe Videotron Ltee", "org": "Videotron Ltee",
        #  "as": "AS5769 Videotron Ltee", "query": "24.48.0.1"}
        geolocation.logger.debug("Starting geolocation")

        if query_type == QueryType.URL:
            query = extract_domain(query)
            geolocation.logger.debug(
                f"Extracted domain from URL: {query}, running geolocation on "
                f"it as {query}")
        res = requests.get(f"http://ip-api.com/json/{query}")
        if res.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch geolocation data for {query}: {res.text}")
        data = res.json()
        if data['status'] != 'success':
            raise RuntimeError(
                f"Geolocation query failed for {query}: {res.text}")
        geolocation.logger.debug(
            f"Geolocation data fetched successfully for {query}")
        lat = data.get('lat', 0.0)
        lon = data.get('lon', 0.0)
        html = (
            "<h2>Geolocation Information</h2>"
            f"<p>Looks to be located in {data.get('city', 'unknown')}, "
            f"{data.get('regionName', 'unknown')}, "
            f"{data.get('country', 'unknown')} ("
            f"{data.get('countryCode', 'unknown')}).</p>"
            "<p>This is not factored into the confidence score as geolcation "
            "is not be reliable.</p>"
            f'<iframe width="100%" height="400" frameborder="0" '
            f'scrolling="no" src="https://www.openstreetmap.org/export/embed'
            f'.html?bbox={lon - 0.5}%2C{lat - 0.5}%2C{lon + 0.5}%2C'
            f'{lat + 0.5}&layer=mapnik&marker={lat}%2C{lon}" '
            f'style="border:0;"></iframe>'

        )
        return Result(
            raw={
                'country': data.get('country'),
                'country_code': data.get('countryCode'),
                'region': data.get('region'),
                'region_name': data.get('regionName'),
                'city': data.get('city'),
                'zip': data.get('zip'),
                'lat': data.get('lat'),
                'lon': data.get('lon'),
                'timezone': data.get('timezone'),
                'isp': data.get('isp'),
                'org': data.get('org'),
                'as': data.get('as')
            },
            timestamp=time.time(),
            certainty=-1,
            message=html
        )

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.IPv6, QueryType.IPv4, QueryType.DOMAIN, QueryType.URL]


if __name__ == '__main__':
    location = geolocation('1.1.1.1', QueryType.IPv4)
    location.run(force_fetch=True)
    print(location.result)
