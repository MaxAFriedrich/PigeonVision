import time
import os

from dotenv import load_dotenv
import requests

from pigeonvision.heuristics.base import Heuristic, Result
from pigeonvision.validate import QueryType


class hybrid_analysis(Heuristic):

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):

        load_dotenv()

        msg = (
            "<h2>Hybrid Analysis</h2>Hybrid Analysis is a tool that uses "
            "CrowdStrike's sandbox "
            "to determine if something is malicious.<br><br> They come up "
            "with a threat "
            "score out of 100 with each query, which we translate into a "
            "percentage score from Hybird Analysis.")

        headers = {
            'api-key': os.environ["HYBRID_KEY"]
        }

        data = {}

        if query_type == QueryType.DOMAIN:
            data['domain'] = query
        elif query_type == QueryType.URL:
            data['url'] = query

        res = requests.post(
            'https://www.hybrid-analysis.com/api/v2/search/terms',
            headers=headers, data=data)

        score = res.json()["result"][0]['threat_score']

        msg += (f"<br><br>Hybird Analysis has assessed that this "
                f"{list(data.keys())[0]} has a threat score of {score}")

        return Result(
            certainty=score / 100,
            raw=res.text,
            message=msg)

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.DOMAIN, QueryType.URL]
