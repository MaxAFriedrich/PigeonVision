import time

from pigeonvision.heuristics.base import Result


class AllHeuristics:
    # These have more than 3000 queries per month
    always = ['spamhaus']
    # These have between 300 and 3000 queries per month
    sometimes = []
    # These have less than 300 queries per month
    rarely = []


def run(query: str, query_type: QueryType) -> Result:
    """
    Runs all heuristics for the given query and query type.

    :param query: The query to be processed.
    :param query_type: The type of the query.
    :return: An aggregated result from the heuristics.
    """
    certainty = 0.0
    messages = []

    return Result(
        certainty=certainty,
        message=' <br>\n'.join(messages),
        raw={},
        timestamp=time.time()
    )
