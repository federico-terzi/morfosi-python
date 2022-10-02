from copy import deepcopy
from typing import Any


def snapshot(value: Any) -> Any:
    return deepcopy(value)
