from pigeonvision.heuristics.urlhaus import urlhaus
from pigeonvision.validate.utils import QueryType

if __name__ == "__main__":
    heuristic = urlhaus(
        "https://pub-7981e858ef724809929147635c295c9b.r2.dev/ultralinvitepart"
        ".exe",
        QueryType.URL)

    print(heuristic.result)
