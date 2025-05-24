import hashlib
import json
import tempfile
from pathlib import Path

from pigeonvision.heuristics.base import Result

CACHE_DIR = Path(tempfile.gettempdir()) / 'pigeonvision_cache'

CACHE_DIR.mkdir(parents=True, exist_ok=True)


def hash_query(query: str, query_type: str) -> str:
    inp = f"{query_type}:{query}".encode('utf-8')
    return hashlib.sha1(inp).hexdigest()


def get_cache(query: str, query_type: str) -> Result | None:
    filename = CACHE_DIR / f"{hash_query(query, query_type)}.cache"
    if not filename.exists():
        return None
    with filename.open('r') as f:
        return Result.from_dict(json.load(f))


def set_cache(query: str, query_type: str, result: Result) -> None:
    filename = CACHE_DIR / f"{hash_query(query, query_type)}.cache"
    with filename.open('w') as f:
        json.dump(result.__dict__, f, default=lambda o: o.__dict__, indent=4)
