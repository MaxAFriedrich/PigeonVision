from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Result:
    certainty: float
    message: str
    raw: dict
    timestamp: float

    def __dict__(self):
        return {
            'certainty': self.certainty,
            'message': self.message,
            'raw': self.raw,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> Result:
        return cls(
            certainty=data.get('certainty', 0.0),
            message=data.get('message', ''),
            raw=data.get('raw', {}),
            timestamp=data.get('timestamp', 0)
        )
