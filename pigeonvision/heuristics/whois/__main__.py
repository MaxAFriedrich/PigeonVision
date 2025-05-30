from pigeonvision.heuristics.whois import whois
from pigeonvision.validate.utils import QueryType

if __name__ == "__main__":
    heuristic = whois("google.com", QueryType.DOMAIN)
    print(heuristic.result)
