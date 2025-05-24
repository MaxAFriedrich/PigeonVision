from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Result:
    is_safe: bool
    certainty: float
    message: str
    raw: dict
    timestamp: int

    @classmethod
    def from_dict(cls, data: dict) -> Result:
        return cls(
            is_safe=data.get('is_safe', False),
            certainty=data.get('certainty', 0.0),
            message=data.get('message', ''),
            raw=data.get('raw', {}),
            timestamp=data.get('timestamp', 0)
        )
