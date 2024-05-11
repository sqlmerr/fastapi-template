from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    offset: int = 0
    count: int = 10
