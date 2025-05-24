import importlib

from pigeonvision.heuristics.base import Result, Heuristic
from pigeonvision.validate.utils import QueryType


class AllHeuristics:
    # These have more than 3000 queries per month
    always = [
        ['whois', 1],
        ['dns_lookup', 1],
        ['spf', 1],
        ['dkim', 1],
        ['dmarc', 1],
        ['geolocation', 0.7],
        ['spamhaus', 0.8],
        ['virus_total', 0.95],
        ['hybrid_analysis', 0.9],
        ['threatfox', 0.8],
        ['safe_browsing', 0.9],
        ['abuseipdb', 0.9],
        ['urlhaus', 0.8],
        ['censys', 0.9],
    ]
    # These have between 300 and 3000 queries per month
    sometimes = [
        ['alienvault', 0.5],
        ['team_cymru', 0.5],
    ]
    # These have less than 300 queries per month
    rarely = [
        ['blacklist_checker', 0.8]
    ]


def add_imports(array) -> list:
    for i in range(len(array)):
        heuristic_name, _ = array[i]
        module = importlib.import_module(
            'pigeonvision.heuristics.' + heuristic_name)
        heuristic = getattr(module, heuristic_name)
        array.append(heuristic)
    return array


AllHeuristics.always = add_imports(AllHeuristics.always)
AllHeuristics.sometimes = add_imports(AllHeuristics.sometimes)
AllHeuristics.rarely = add_imports(AllHeuristics.rarely)


def mean_certainty(
        reliability: list[float],
        trustworthiness: list[float]
) -> float:
    return sum(reliability) / sum(trustworthiness)


def calculate_reliability(certainty: float, trustworthiness: float) -> float:
    return certainty * trustworthiness


def have_enough_data(
        reliabilities: list[float],
        trustworthiness: list[float],
) -> bool:
    if len(reliabilities) < 4:
        return False
    if mean_certainty(reliabilities, trustworthiness) < 0.5:
        return False
    high_certainty_count = 0
    for reliability in reliabilities:
        if reliability > 0.9:
            high_certainty_count += 1
    if high_certainty_count > 3:
        return True


def run_heuristic_list(
        query: str,
        query_type: QueryType,
        heuristic_list: list,
        reliabilities: list[float],
        trustworthiness: list[float],
        messages: list[str],
) -> (list, list, list):
    # TODO make this multi-threaded
    for heuristic_name, trustworthiness_value, heuristic in heuristic_list:

        if have_enough_data(reliabilities, trustworthiness):
            return reliabilities, trustworthiness, messages
        if query_type not in heuristic.allowed_query_types():
            continue

        try:
            heuristic_instance: Heuristic = heuristic(query, query_type)
        except Exception as e:
            messages.append(f"{heuristic_name} failed: {str(e)}")
            continue

        result = heuristic_instance.result
        if not isinstance(result, Result):
            messages.append(f"{heuristic_name} did not return a valid result.")
            continue

        reliability = calculate_reliability(result.certainty,
                                            trustworthiness_value)
        reliabilities.append(reliability)
        trustworthiness.append(trustworthiness_value)
        messages.append(result.message)

    return reliabilities, trustworthiness, messages


def run(query: str, query_type: QueryType) -> (float, str):
    """
    Runs all heuristics for the given query and query type.

    :param query: The query to be processed.
    :param query_type: The type of the query.
    :return: An aggregated result from the heuristics.
    """
    reliabilities = []
    trustworthiness = []
    messages = []

    # Run heuristics that are always run
    reliabilities, trustworthiness, messages = run_heuristic_list(
        query, query_type, AllHeuristics.always,
        reliabilities, trustworthiness, messages
    )
    # Run heuristics that are sometimes run
    reliabilities, trustworthiness, messages = run_heuristic_list(
        query, query_type, AllHeuristics.sometimes,
        reliabilities, trustworthiness, messages
    )
    # Run heuristics that are rarely run
    reliabilities, trustworthiness, messages = run_heuristic_list(
        query, query_type, AllHeuristics.rarely,
        reliabilities, trustworthiness, messages
    )

    return (
        mean_certainty(reliabilities, trustworthiness),
        ' <br>\n'.join(messages)
    )
