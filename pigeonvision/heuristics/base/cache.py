import hashlib
import json
import tempfile
from pathlib import Path

from pigeonvision.heuristics.base.result import Result

__ALL__ = ['get', 'set', 'CACHE_TIMEOUT']

CACHE_DIR = Path(tempfile.gettempdir()) / 'pigeonvision_cache'

CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Timeout cache after 3 days
CACHE_TIMEOUT = 60 * 60 * 24 * 3


def hash_query(query: str, query_type: str) -> str:
    inp = f"{query_type}:{query}".encode('utf-8')
    return hashlib.sha1(inp).hexdigest()


def get(query: str, query_type: str) -> Result | None:
    filename = CACHE_DIR / f"{hash_query(query, query_type)}.cache"
    if not filename.exists():
        return None
    with filename.open('r') as f:
        return Result.from_dict(json.load(f))


def set(query: str, query_type: str, result: Result) -> None:
    filename = CACHE_DIR / f"{hash_query(query, query_type)}.cache"
    out = json.dumps(result.__dict__())
    with filename.open('w') as f:
        f.write(out)
