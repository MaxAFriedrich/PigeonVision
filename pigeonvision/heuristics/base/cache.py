from pathlib import Path

from pigeonvision.heuristics.base import Result

CACHE_DIR = Path("/tmp/pigeonvision_cache")

CACHE_DIR.mkdir(parents=True, exist_ok=True)

CacheObject = list[tuple[int, Result]]

def get_cache(query: str, query_type: str) -> CacheObject:
    return [(1, Result(is_safe=True, certainty=1.0, message="Cached result", raw={}))]

def set_cache(query: str, query_type: str, result: Result) -> None:
    pass
