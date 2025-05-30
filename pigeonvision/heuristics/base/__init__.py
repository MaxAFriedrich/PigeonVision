from abc import ABC, abstractmethod
from dataclasses import dataclass

from pigeonvision.validate import QueryType

__ALL__ = ["Heuristic", "Result"]


class Heuristic(ABC):

    def __init__(self, query: str, query_type: QueryType):
        self.query = query
        self.query_type = query_type
        self.result = None
        self.run()

    def run(self, force_fetch: bool = False) -> Result:
        self.result = self.fetch(self.query, self.query_type)

        return self.result

    @staticmethod
    @abstractmethod
    def fetch(query: str, query_type: QueryType) -> Result:
        """
        Fetches the result from the heuristic.

        :param query: The query to be processed.
        :param query_type: The type of the query.
        :return: Result object containing the heuristic's findings.
        """
        pass

    @staticmethod
    @abstractmethod
    def allowed_query_types() -> list[QueryType]:
        """
        Returns a list of allowed query types for this heuristic.

        :return: List of QueryType enums that this heuristic supports.
        """
        pass


@dataclass
class Result:
    certainty: float
    message: str
    raw: dict

    def __dict__(self):
        return {
            "certainty": self.certainty,
            "message": self.message,
            "raw": self.raw,
        }
