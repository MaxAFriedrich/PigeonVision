import hashlib
import json
import logging

from pigeonvision import persistent
from pigeonvision.heuristics.base.result import Result

__ALL__ = ['get', 'set', 'CACHE_TIMEOUT']

# Timeout cache after 3 days
CACHE_TIMEOUT = 60 * 60 * 24 * 3

logger = logging.getLogger(__name__)


def hash_query(query: str, query_type: str, heuristic: str) -> str:

    inp = f"{query_type}:{heuristic}:{query}".encode('utf-8')
    return hashlib.sha1(inp).hexdigest()


def get(query: str, query_type: str, heuristic: str) -> Result | None:
    filename = (persistent.LOCAL_CACHE /
                f"{hash_query(query, query_type, heuristic)}.cache")

    logger.debug("Querying cache for %s", filename)
    if not filename.exists():
        logger.debug("Cache miss")
        return None
    with filename.open('r') as f:
        logger.debug("Cache hit")
        return Result.from_dict(json.load(f))


def set(query: str, query_type: str, heuristic: str, result: Result) -> None:
    filename = (persistent.LOCAL_CACHE /
                f"{hash_query(query, query_type, heuristic)}.cache")
    logger.debug("Cacheing results in %s", filename)
    out = json.dumps(result.__dict__())
    with filename.open('w') as f:
        f.write(out)
