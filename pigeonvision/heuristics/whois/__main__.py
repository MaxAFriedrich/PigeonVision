from pigeonvision.heuristics.whois import whois
from pigeonvision.validate.utils import QueryType

if __name__ == "__main__":
    heuristic = whois("ns2.berthons.se", QueryType.DOMAIN)

    print(heuristic.result)