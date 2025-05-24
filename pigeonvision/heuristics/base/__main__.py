import time

from pigeonvision.heuristics.base import Result, Heuristic
from pigeonvision.validate import QueryType


def test():
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

    # Example usage
    assert QueryType.MD5 in TestHeuristic.allowed_query_types()
    heuristic = TestHeuristic("Sample Heuristic", QueryType.MD5)
    result = heuristic.result.__dict__()
    assert heuristic.run().__dict__() == result


if __name__ == '__main__':
    test()
