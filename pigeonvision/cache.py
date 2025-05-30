import hashlib
import json
import logging
from dataclasses import dataclass

from pigeonvision import persistent

# Timeout cache after 3 days
CACHE_TIMEOUT = 60 * 60 * 24 * 3

logger = logging.getLogger(__name__)


@dataclass
class CacheResult:
    summary: str
    long: str
    certainty: float
    timestamp: int

    def __dict__(self):
        return {
            "summary": self.summary,
            "long": self.long,
            "certainty": self.certainty,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, cache_result):
        return cls(
            summary=cache_result['summary'],
            long=cache_result['long'],
            certainty=cache_result['certainty'],
            timestamp=cache_result['timestamp']
        )


def hash_query(query: str, query_type: str) -> str:
    inp = f"{query_type}:{query}".encode('utf-8')
    return hashlib.sha1(inp).hexdigest()


def get(query: str, query_type: str) -> CacheResult | None:
    filename = (persistent.LOCAL_CACHE /
                f"{hash_query(query, query_type)}.cache")
    logger.debug("Querying cache for %s", filename)
    if not filename.exists():
        logger.debug("Cache miss")
        return None
    with filename.open('r') as f:
        logger.debug("Cache hit")
        cache_result = CacheResult.from_dict(json.load(f))
    if cache_result.timestamp > CACHE_TIMEOUT:
        logger.debug("Expired cache entry")
    return cache_result


def set(query: str, query_type: str, cache_result: CacheResult) -> None:
    filename = (persistent.LOCAL_CACHE /
                f"{hash_query(query, query_type)}.cache")
    logger.debug(f"Cacheing results in {filename}")
    out = json.dumps(cache_result.__dict__())
    with filename.open('w') as f:
        f.write(out)


__ALL__ = [get, set, CacheResult]
