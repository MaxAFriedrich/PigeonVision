import requests
import os
import time
import math

from dotenv import load_dotenv

from pigeonvision.heuristics.base.result import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate.utils import QueryType

class spamhaus(Heuristic):

    auth_token = ''
    auth_attempts = 0

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def acquire_auth():

        load_dotenv()

        spamhaus.auth_attempts += 1

        if spamhaus.auth_attempts > 3: raise RuntimeError("Spamhaus authentication attempt limit reached")

        data = f'{{"username": "{os.environ['SPAMHAUS_USER']}", "password": "{os.environ['SPAMHAUS_PASS']}", "realm":"intel"}}'

        res = requests.post('https://api.spamhaus.org/api/v1/login', data=data)

        if res.status_code == 200:
            
            spamhaus.auth_attempts = 0
            spamhaus.auth_token = res.json()["token"]

    @staticmethod
    def fetch_domain(query: str) -> Result:
        headers = {"Authorization": f"Bearer {spamhaus.auth_token}"}
        
        res = requests.get(f"https://api.spamhaus.org/api/intel/v2/byobject/domain/{query}", headers=headers)

    @staticmethod
    def fetch_IP(query: str) -> Result:
        headers = {"Authorization": f"Bearer {spamhaus.auth_token}"}

        res = requests.get(f"https://api.spamhaus.org/api/intel/v2/byobject/domain/{query}", headers=headers)
        pass

    @staticmethod
    def fetch(query: str, query_type: QueryType) -> Result:

        if spamhaus.auth_token == '': spamhaus.acquire_auth()
        
        if query_type == QueryType.IPv4 or query_type == QueryType.IPv6:
            return spamhaus.fetch_IP(query)

        elif query_type == QueryType.DOMAIN:
            return spamhaus.fetch_domain(query)

        print(res)

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        return [QueryType.MD5, QueryType.SHA1, QueryType.URL, QueryType.DOMAIN]

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