from pigeonvision.heuristics.dns_lookup import dns_lookup
from pigeonvision.validate.utils import QueryType

if __name__ == "__main__":
    heuristic = dns_lookup("tom-blue.co", QueryType.DOMAIN)

    print(heuristic.result)
