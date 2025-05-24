from dataclasses import dataclass


@dataclass
class Result:
    is_safe: bool
    certainty: float
    message: str
    raw: dict

