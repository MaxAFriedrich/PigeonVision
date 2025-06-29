from pigeonvision.heuristics.hybrid_analysis import hybrid_analysis
from pigeonvision.validate.utils import QueryType

if __name__ == "__main__":
    heuristic = hybrid_analysis("kaspersky-secure.ru", QueryType.DOMAIN)

    print(heuristic.result)
