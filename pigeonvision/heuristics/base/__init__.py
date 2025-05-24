from abc import ABC, abstractmethod

from pigeonvision.heuristics.base.result import Result
from pigeonvision.validate import QueryType

__ALL__ = ["Heuristic", "Result"]


class Heuristic(ABC):

    def __init(self, query: str, query_type: QueryType):
        self.query = query
        self.query_type = query_type
        self.result = None
        self.run()

    def run(self, force_fetch: bool = False) -> Result:
        # Checking force fetch first to avoid unnecessary cache checks
        if force_fetch:
            self.result = self.fetch(self.query, self.query_type)
        elif not self.get_cache():
            self.result = self.fetch(self.query, self.query_type)
        
        self.save_cache()

        return self.result

    def get_cache(self) -> bool:
        """
        Checks if the result is cached, and then writes the cached result to
        result.

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
