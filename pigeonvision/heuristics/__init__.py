from pigeonvision.validate.utils import QueryType
from pigeonvision.heuristics.base import Result


class AllHeuristics:
    # These have more than 3000 queries per month
    always = [
        ('whois', 1),
        ('dns_lookup', 1),
        ('spf', 1),
        ('dkim', 1),
        ('dmarc', 1),
        ('geolocation', 0.7),
        ('spamhaus', 0.8),
        ('virus_total', 0.95),
        ('hybrid_analysis', 0.9),
        ('threatfox', 0.8),
        ('safe_browsing', 0.9),
        ('abuseipdb', 0.9),
        ('urlhaus', 0.8),
        ('censys', 0.9),
    ]
    # These have between 300 and 3000 queries per month
    sometimes = [
        ('alienvault', 0.5),
        ('team_cymru', 0.5),
    ]
    # These have less than 300 queries per month
    rarely = [
        ('blacklist_checker', 0.8)
    ]


def run(query: str, query_type: QueryType) -> (float, str):
    """
    Runs all heuristics for the given query and query type.

    :param query: The query to be processed.
    :param query_type: The type of the query.
    :return: An aggregated result from the heuristics.
    """
    certainty = 0.0
    messages = []

    return (
        certainty,
        ' <br>\n'.join(messages)
    )
