import traceback
from typing import Any, Optional
import wrapt

from morfosi.registry import DEFAULT_REGISTRY, Registry
from morfosi.schema import Path


class BaseTracer(wrapt.ObjectProxy):
    def __init__(
        self, wrapped: Any, registry: Optional[Registry] = None, path: Path = []
    ):
        super().__init__(wrapped)

        self._tracer_registry = registry if registry else DEFAULT_REGISTRY
        self._tracer_path = path

    def resolve_path(self, name: str) -> Path:
        if len(self._tracer_path) > 0:
            return self._tracer_path + [name]
        else:
            return [name]

    def resolve_stack(self) -> str:
        return traceback.format_stack()
