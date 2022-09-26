from dataclasses import dataclass
from typing import Any, List, Union

Path = List[Union[str, int]]


@dataclass(frozen=True)
class Add:
    path: Path
    new_value: Any
    stack: str


@dataclass(frozen=True)
class Change:
    path: Path
    old_value: Any
    new_value: Any
    stack: str


@dataclass(frozen=True)
class Delete:
    path: Path
    old_value: Any
    stack: str


Action = Union[Add, Change, Delete]
