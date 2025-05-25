import time
from abc import ABC, abstractmethod

from pigeonvision.heuristics.base import cache
from pigeonvision.heuristics.base.result import Result
from pigeonvision.validate import QueryType

__ALL__ = ["Heuristic", "Result"]


class Heuristic(ABC):

    def __init__(self, query: str, query_type: QueryType):
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
        heuristic_name = self.__class__.__name__
        res = cache.get(self.query, self.query_type.value, heuristic_name)
        if not isinstance(res, Result):
            return False
        if res.timestamp + cache.CACHE_TIMEOUT < time.time():
            return False
        self.result = res
        return True

    def save_cache(self) -> None:
        """
        Saves the current result to the cache.

        :return: None
        """
        if self.result:
            heuristic_name = self.__class__.__name__
            cache.set(self.query, self.query_type.value, heuristic_name,
                      self.result)
        else:
            raise ValueError("Result is not set. Cannot save to cache.")

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
