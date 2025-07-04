import importlib
import logging

from pigeonvision.heuristics.base import Result, Heuristic
from pigeonvision.validate.utils import QueryType


class AllHeuristics:
    # These have more than 3000 queries per month
    always = [
        ['safe_browsing', 0.9],
        ['spamhaus', 0.8],
        ['virus_total', 0.95],
        ['hybrid_analysis', 0.9],
        ['dns_lookup', 0.4],
        ['geolocation', 0.7],
        ['whois', 1],
        ['threatfox', 0.8],
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

    logger = logging.getLogger(__name__)


def add_imports(array) -> list:
    for i in range(len(array)):
        heuristic_name, _ = array[i]
        AllHeuristics.logger.debug("Importing heuristic module %s",
                                   'pigeonvision.heuristics.' + heuristic_name)
        module = importlib.import_module(
            'pigeonvision.heuristics.' + heuristic_name)
        heuristic = getattr(module, heuristic_name)
        array[i].append(heuristic)
    return array


AllHeuristics.always = add_imports(AllHeuristics.always)
AllHeuristics.sometimes = add_imports(AllHeuristics.sometimes)
AllHeuristics.rarely = add_imports(AllHeuristics.rarely)


def mean_certainty(
        reliability: list[float],
        trustworthiness: list[float]
) -> float:
    total_reliability = sum(reliability)
    total_trustworthiness = sum(trustworthiness)

    AllHeuristics.logger.debug("Total reliability: %f", total_reliability)
    AllHeuristics.logger.debug("Total reliability: %f", total_trustworthiness)
    if total_trustworthiness == 0 or total_reliability == 0:
        return 0.0
    return total_reliability / total_trustworthiness


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
    return False


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
        try:
            if query_type not in heuristic.allowed_query_types():
                continue
        except NotImplementedError:
            continue

        try:
            heuristic_instance: Heuristic = heuristic(query, query_type)
        except Exception as e:
            AllHeuristics.logger.error(
                f"Error initializing heuristic {heuristic_name}: {str(e)}")
            continue

        result = heuristic_instance.result
        if not isinstance(result, Result):
            messages.append(f"{heuristic_name} did not return a valid result.")
            continue
        print(
            f"Running heuristic: {heuristic_name} with trustworthiness "
            f"{trustworthiness_value}, with result: {result.certainty}")
        messages.append(result.message)

        if result.certainty == -1:
            continue

        reliability = calculate_reliability(result.certainty,
                                            trustworthiness_value)
        reliabilities.append(reliability)
        trustworthiness.append(trustworthiness_value)

    return reliabilities, trustworthiness, messages


def run_all(self, queries: list | str, query_type: QueryType) -> (float, str):
    all_reliabilities = []
    all_trustworthiness = []
    all_messages = []

    for query in queries:
        rel, trust, msg = run_heuristics(query, query_type)

        self.logger.debug("%s resulted in %f %f %s", query, rel, trust, msg)

        all_reliabilities.append(rel)
        all_trustworthiness.append(trust)
        all_messages.append(msg)

    final_reliabilities = []
    final_trustworthiness = []
    final_messages = []

    for reliability, trustworthiness, messages in zip(all_reliabilities,
                                                      all_trustworthiness,
                                                      all_messages):
        final_reliabilities.append(max(reliability))
        final_trustworthiness.append(
            trustworthiness[reliability.index(max(reliability))])
        final_messages.append(messages[reliability.index(max(reliability))])

    return (
        final_reliabilities,
        final_trustworthiness,
        final_messages
    )


def run_heuristics(query: str, query_type: QueryType) -> (list, list, list):
    reliabilities = []
    trustworthiness = []
    messages = []

    # Run heuristics that are always run
    AllHeuristics.logger.debug("Starting always heuristics")
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
    AllHeuristics.logger.info(
        "Not enough confidence, running rarely heuristics")
    reliabilities, trustworthiness, messages = run_heuristic_list(
        query, query_type, AllHeuristics.rarely,
        reliabilities, trustworthiness, messages
    )

    return reliabilities, trustworthiness, messages


def run(query: str, query_type: QueryType) -> (float, str):
    """
    Runs all heuristics for the given query and query type.

    :param query: The query to be processed.
    :param query_type: The type of the query.
    :return: An aggregated result from the heuristics.
    """
    reliabilities, trustworthiness, messages = run_heuristics(query, query_type)

    final_certainty = mean_certainty(reliabilities, trustworthiness)

    AllHeuristics.logger.info("Heuristics complete, mean certainty of %f",
                              final_certainty)

    return (
        final_certainty,
        ' <br>\n'.join(messages)
    )
