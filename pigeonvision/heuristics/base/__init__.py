from abc import ABC, abstractmethod
from dataclasses import dataclass

from pigeonvision.validate import QueryType


@dataclass
class Result:
    is_safe: bool
    certainty: float
    message: str
    raw: dict


class Heuristic(ABC):

    def __init(self, query: str, query_type: QueryType):
        self.query = query
        self.query_type = query_type
        
        self.run()

    def run(self, force_fetch: bool = False) -> Result:
        pass

    def get_cache(self) -> bool:
        """
        Checks if the result is cached, and then writes the cached result to result.

        :return: True if the result is cached, False otherwise.
        """
        return False

    def save_cache(self) -> None:
        pass

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
