from typing import Any, Dict, Optional

from morfosi.schema import Change, Add, Delete, Path, TracerOptions
from morfosi.registry import Registry
from morfosi.tracing.base import BaseTracer
from morfosi.tracing.utils import is_primitive, is_morfosi_builtin
from morfosi.tracing.snapshot import snapshot


class DictTracer(BaseTracer):
    def __init__(
        self,
        wrapped: Any,
        registry: Optional[Registry] = None,
        path: Path = [],
        options: TracerOptions = TracerOptions(),
    ):
        super().__init__(wrapped, registry=registry, path=path, options=options)

        from morfosi.tracing.trace import traceable

        for field, value in wrapped.items():
            if not is_primitive(value) and not is_morfosi_builtin(field):
                wrapped[field] = traceable(
                    value, registry=registry, path=path + [field], options=options
                )
                pass

    def __setitem__(self, key: str, value: Any):
        path = self.resolve_path(key)
        stack = self.resolve_stack()
        wrapped: Dict[str, Any] = self.__wrapped__  # type: ignore

        value_snapshot = snapshot(
            value, self._self_tracer_options.value_snapshot_strategy
        )

        if key in wrapped:
            action = Change(
                path=path,
                old_value=snapshot(
                    wrapped[key], self._self_tracer_options.value_snapshot_strategy
                ),
                new_value=value_snapshot,
                stack=stack,
            )
        else:
            action = Add(path=path, new_value=value_snapshot, stack=stack)

        if not is_primitive(value):
            from morfosi.tracing.trace import traceable

            value = traceable(
                value,
                registry=self._self_tracer_registry,
                path=path,
                options=self._self_tracer_options,
            )

        self._self_tracer_registry.append(action)

        return super().__setitem__(key, value)  # type: ignore

    def __delitem__(self, key: str):
        path = self.resolve_path(key)
        stack = self.resolve_stack()

        wrapped: Dict[str, Any] = self.__wrapped__  # type: ignore
        old_value = wrapped.get(key)

        self._self_tracer_registry.append(
            Delete(
                path=path,
                old_value=snapshot(
                    old_value, self._self_tracer_options.value_snapshot_strategy
                ),
                stack=stack,
            )
        )

        return super().__delitem__(key)  # type: ignore
