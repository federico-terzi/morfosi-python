from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class Add:
    path: List[str]
    new_value: Any
    stack: str


@dataclass(frozen=True)
class Change:
    path: List[str]
    old_value: Any
    new_value: Any
    stack: str


@dataclass(frozen=True)
class Delete:
    path: List[str]
    old_value: Any
    stack: str
