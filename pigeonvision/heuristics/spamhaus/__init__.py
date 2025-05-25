import logging
import math
import os
import time

import requests
from dotenv import load_dotenv

from pigeonvision.heuristics.base import Heuristic
from pigeonvision.heuristics.base.result import Result
from pigeonvision.heuristics.spamhaus.spamhaus_tags import tag_messages
from pigeonvision.validate.utils import QueryType, extract_domain


class spamhaus(Heuristic):
    auth_token = ''
    auth_attempts = 0

    logger = logging.getLogger(__name__)

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def acquire_auth():

        spamhaus.logger.debug("Populating spamhaus authentication token")

        load_dotenv()

        spamhaus.auth_attempts += 1

        if spamhaus.auth_attempts > 3: raise RuntimeError(
            "Spamhaus authentication attempt limit reached")

        data = (f'{{"username": "{os.environ["SPAMHAUS_USER"]}", "password": '
                f'"{os.environ["SPAMHAUS_PASS"]}", "realm":"intel"}}')

        res = requests.post('https://api.spamhaus.org/api/v1/login', data=data)

        if res.status_code == 200:
            spamhaus.logger.debug(
                "Spamhaus authentication successful in %i attempts",
                spamhaus.auth_attempts)
            spamhaus.auth_attempts = 0
            spamhaus.auth_token = res.json()["token"]

    @staticmethod
    def fetch_domain(query: str) -> Result:
        headers = {"Authorization": f"Bearer {spamhaus.auth_token}"}

        spamhaus.logger.debug(
            "Querying https://api.spamhaus.org/api/intel/v2/byobject/domain/%s",
            query)

        msg = ("<h2>Spamhaus</h2>"
               "<p>Spamhaus provides a score for domain reputation "
               "where 0 is neutral, positive numbers are good and negative "
               "are bad. "
               "We've done some curve fitting to turn this score into a "
               "confidence interval. <br><br>")

        res = requests.get(
            f"https://api.spamhaus.org/api/intel/v2/byobject/domain/{query}",
            headers=headers)

        score = int(res.json().get('score', 0))
        spamhaus.logger.debug("Spamhaus score: %i", score)

        # https://www.desmos.com/calculator/b7ju6aaz57 to understand this curve
        normalised = (-(score / 2) / math.sqrt(25 + (score ** 2))) + 0.5
        spamhaus.logger.debug("Normalised percentage: %i", normalised)

        msg += (
            f"Spamhaus give this a score of {score}, which we've turned "
            f"into a malicious confidence value of {normalised:.2f}<br><br>"
        )

        for tag in res.json().get('tags', []):
            spamhaus.logger.debug("Found tag %s", tag)
            if tag in tag_messages:
                msg += (tag_messages[tag]) + '<br>'

        msg += '</p>'

        return Result(
            certainty=normalised,
            raw={"data": res.text},
            timestamp=time.time(),
            message=msg
        )

    @staticmethod
    def fetch(query: str, query_type: QueryType) -> Result:
        if query_type in [QueryType.URL, QueryType.EMAIL]:
            query = extract_domain(query)

        spamhaus.logger.info("Starting spamhaus heuristic")

        if spamhaus.auth_token == '':
            spamhaus.acquire_auth()

        return spamhaus.fetch_domain(query)

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.URL, QueryType.DOMAIN,
                QueryType.EMAIL]


'''
    class TestHeuristic(Heuristic):

        def __init__(self, query: str, query_type: QueryType):
            super().__init__(query, query_type)

        @staticmethod
        def fetch(query: str, query_type: QueryType):
            # Simulate fetching data
            return Result(
                is_safe=True,
                certainty=0.95,
                message="This is a test heuristic result.",
                raw={"query": query, "type": query_type.value},
                timestamp=time.time(),
            )

        @staticmethod
        def allowed_query_types() -> list[QueryType]:
            return [QueryType.MD5, QueryType.SHA1, QueryType.URL]
            '''
