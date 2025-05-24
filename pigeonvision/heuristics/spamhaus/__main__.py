from pigeonvision.heuristics.spamhaus import spamhaus
from pigeonvision.validate.utils import QueryType

if __name__ == "__main__":
    heuristic = spamhaus("gmail.com", QueryType.DOMAIN)

    print(heuristic.result)