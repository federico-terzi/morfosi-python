from typing import List

from .schema import Action


class Registry:
    def __init__(self) -> None:
        self.changes: List[Action] = []

    def append(self, change: Action) -> None:
        self.changes.append(change)


DEFAULT_REGISTRY = Registry()
