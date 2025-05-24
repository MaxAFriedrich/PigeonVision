import time

from pigeonvision.heuristics import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType


class alienvault(Heuristic):

    def __init__(self, query: str, query_type: QueryType):
        super().__init__(query, query_type)

    @staticmethod
    def fetch(query: str, query_type: QueryType):
        # Simulate fetching data
        raise NotImplementedError(
            "This is a test heuristic and does not implement fetch.")

    @staticmethod
    def allowed_query_types() -> list[QueryType]:
        raise NotImplementedError(
            "This is a test heuristic and does not implement "
            "allowed_query_types.")
