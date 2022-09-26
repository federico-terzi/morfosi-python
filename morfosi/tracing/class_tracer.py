from typing import Any, Optional

from morfosi.schema import Change, Add, Delete, Path
from morfosi.registry import Registry
from morfosi.tracing.base import BaseTracer
from morfosi.tracing.utils import is_primitive, is_morfosi_builtin


class ClassTracer(BaseTracer):
    def __init__(
        self, wrapped: Any, registry: Optional[Registry] = None, path: Path = []
    ):
        super().__init__(wrapped, registry=registry, path=path)

        from morfosi.tracing.trace import traceable

        for field, value in wrapped.__dict__.items():
            if not is_primitive(value) and not is_morfosi_builtin(field):
                wrapped.__dict__[field] = traceable(
                    value, registry=registry, path=path + [field]
                )
                pass

    def __setattr__(self, name: str, value: Any):
        if is_morfosi_builtin(name):
            return super().__setattr__(name, value)  # type: ignore

        path = self.resolve_path(name)
        stack = self.resolve_stack()

        if name in self.__dict__:
            action = Change(
                path=path, old_value=self.__dict__[name], new_value=value, stack=stack
            )
        else:
            action = Add(path=path, new_value=value, stack=stack)

        self.__dict__["_tracer_registry"].append(action)

        return super().__setattr__(name, value)  # type: ignore

    def __delattr__(self, name: str):
        path = self.resolve_path(name)
        stack = self.resolve_stack()
        old_value = self.__dict__.get(name)

        self.__dict__["_tracer_registry"].append(
            Delete(path=path, old_value=old_value, stack=stack)
        )

        return super().__delattr__(name)  # type: ignore
