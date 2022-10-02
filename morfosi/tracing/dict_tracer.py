from typing import Any, Dict, Optional

from morfosi.schema import Change, Add, Delete, Path
from morfosi.registry import Registry
from morfosi.tracing.base import BaseTracer
from morfosi.tracing.utils import is_primitive, is_morfosi_builtin


class DictTracer(BaseTracer):
    def __init__(
        self, wrapped: Any, registry: Optional[Registry] = None, path: Path = []
    ):
        super().__init__(wrapped, registry=registry, path=path)

        from morfosi.tracing.trace import traceable

        for field, value in wrapped.items():
            if not is_primitive(value) and not is_morfosi_builtin(field):
                wrapped[field] = traceable(
                    value, registry=registry, path=path + [field]
                )
                pass

    def __setitem__(self, key: str, value: Any):
        path = self.resolve_path(key)
        stack = self.resolve_stack()
        wrapped: Dict[str, Any] = self.__wrapped__  # type: ignore

        if key in wrapped:
            action = Change(
                path=path, old_value=wrapped[key], new_value=value, stack=stack
            )
        else:
            action = Add(path=path, new_value=value, stack=stack)

        self._self_tracer_registry.append(action)

        return super().__setitem__(key, value)  # type: ignore

    def __delitem__(self, key: str):
        path = self.resolve_path(key)
        stack = self.resolve_stack()

        wrapped: Dict[str, Any] = self.__wrapped__  # type: ignore
        old_value = wrapped.get(key)

        self._self_tracer_registry.append(
            Delete(path=path, old_value=old_value, stack=stack)
        )

        return super().__delitem__(key)  # type: ignore
