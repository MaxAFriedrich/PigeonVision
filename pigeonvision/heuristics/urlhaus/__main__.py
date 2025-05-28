from pigeonvision.heuristics.urlhaus import urlhaus
from pigeonvision.validate.utils import QueryType

if __name__ == "__main__":
    heuristic = urlhaus("https://nk.zujer.ru/wvdb.sh", QueryType.URL)

    print(heuristic.result)