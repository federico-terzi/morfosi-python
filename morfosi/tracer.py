import traceback
from typing import List, Optional
import wrapt

from morfosi.schema import Change, Add, Delete
from morfosi.registry import Registry, DEFAULT_REGISTRY


class Tracer(wrapt.ObjectProxy):
    def __init__(self, wrapped, registry: Optional[Registry] = None):
        super().__init__(wrapped)

        self._tracer_registry = registry if registry else DEFAULT_REGISTRY

    def __setattr__(self, name, value):
        if name == "_tracer_registry":
            return super().__setattr__(name, value)

        path = self.resolve_path(name)
        stack = self.resolve_stack()

        if name in self.__dict__:
            action = Change(
                path=path, old_value=self.__dict__[name], new_value=value, stack=stack
            )
        else:
            action = Add(path=path, new_value=value, stack=stack)

        self.__dict__["_tracer_registry"].append(action)

        return super().__setattr__(name, value)

    def __delattr__(self, name):
        path = self.resolve_path(name)
        stack = self.resolve_stack()
        old_value = self.__dict__.get(name)

        self.__dict__["_tracer_registry"].append(
            Delete(path=path, old_value=old_value, stack=stack)
        )

        return super().__delattr__(name)

    def resolve_path(self, name: str) -> List[str]:
        # TODO: nested paths
        return [name]

    def resolve_stack(self) -> str:
        return traceback.format_stack()
