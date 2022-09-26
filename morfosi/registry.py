from typing import List

from .schema import Change


class Registry:
    def __init__(self) -> None:
        self.changes: List[Change] = []

    def append(self, change: Change) -> None:
        self.changes.append(change)


DEFAULT_REGISTRY = Registry()
