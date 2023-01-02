from typing import Any, List, Optional

from morfosi.schema import Change, Add, Delete, Path, TracerOptions
from morfosi.registry import Registry
from morfosi.tracing.base import BaseTracer
from morfosi.tracing.utils import is_primitive
from morfosi.tracing.snapshot import snapshot


class ListTracer(BaseTracer):
    def __init__(
        self,
        wrapped: Any,
        registry: Optional[Registry] = None,
        path: Path = [],
        options: TracerOptions = TracerOptions(),
    ):
        super().__init__(wrapped, registry=registry, path=path, options=options)

        from morfosi.tracing.trace import traceable

        for index, value in enumerate(wrapped):
            if not is_primitive(value):
                wrapped[index] = traceable(
                    value, registry=registry, path=path + [index], options=options
                )
                pass

    def __setitem__(self, index: int, value: Any):
        path = self.resolve_path(index)
        stack = self.resolve_stack()
        wrapped: List[Any] = self.__wrapped__  # type: ignore

        value_snapshot = snapshot(
            value, self._self_tracer_options.value_snapshot_strategy
        )

        if index < len(wrapped):
            action = Change(
                path=path,
                old_value=snapshot(
                    wrapped[index], self._self_tracer_options.value_snapshot_strategy
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

        return super().__setitem__(index, value)  # type: ignore

    def __delitem__(self, index: int):
        path = self.resolve_path(index)
        stack = self.resolve_stack()

        wrapped: List[Any] = self.__wrapped__  # type: ignore
        old_value = wrapped[index]

        self._self_tracer_registry.append(
            Delete(
                path=path,
                old_value=snapshot(
                    old_value, self._self_tracer_options.value_snapshot_strategy
                ),
                stack=stack,
            )
        )

        return super().__delitem__(index)  # type: ignore

    def append(self, value: Any):
        wrapped: List[Any] = self.__wrapped__  # type: ignore
        path = self.resolve_path(len(wrapped))
        stack = self.resolve_stack()

        value_snapshot = snapshot(
            value, self._self_tracer_options.value_snapshot_strategy
        )

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

        return wrapped.append(value)  # type: ignore


# For reference, to be implemented
# @overload
# def __init__(self) -> None: ...
# @overload
# def __init__(self, __iterable: Iterable[_T]) -> None: ...
# def copy(self) -> list[_T]: ...
# def append(self, __object: _T) -> None: ...
# def extend(self, __iterable: Iterable[_T]) -> None: ...
# def pop(self, __index: SupportsIndex = ...) -> _T: ...
# # Signature of `list.index` should be kept in line with `collections.UserList.index()`
# # and multiprocessing.managers.ListProxy.index()
# def index(self, __value: _T, __start: SupportsIndex = ..., __stop: SupportsIndex = ...) -> int: ...
# def count(self, __value: _T) -> int: ...
# def insert(self, __index: SupportsIndex, __object: _T) -> None: ...
# def remove(self, __value: _T) -> None: ...
# # Signature of `list.sort` should be kept inline with `collections.UserList.sort()`
# # and multiprocessing.managers.ListProxy.sort()
# #
# # Use list[SupportsRichComparisonT] for the first overload rather than [SupportsRichComparison]
# # to work around invariance
# @overload
# def sort(self: list[SupportsRichComparisonT], *, key: None = ..., reverse: bool = ...) -> None: ...
# @overload
# def sort(self, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = ...) -> None: ...
# def __len__(self) -> int: ...
# def __iter__(self) -> Iterator[_T]: ...
# __hash__: ClassVar[None]  # type: ignore[assignment]
# @overload
# def __getitem__(self, __i: SupportsIndex) -> _T: ...
# @overload
# def __getitem__(self, __s: slice) -> list[_T]: ...
# @overload
# def __setitem__(self, __i: SupportsIndex, __o: _T) -> None: ...
# @overload
# def __setitem__(self, __s: slice, __o: Iterable[_T]) -> None: ...
# def __delitem__(self, __i: SupportsIndex | slice) -> None: ...
# # Overloading looks unnecessary, but is needed to work around complex mypy problems
# @overload
# def __add__(self, __x: list[_T]) -> list[_T]: ...
# @overload
# def __add__(self, __x: list[_S]) -> list[_S | _T]: ...
# def __iadd__(self: Self, __x: Iterable[_T]) -> Self: ...  # type: ignore[misc]
# def __mul__(self, __n: SupportsIndex) -> list[_T]: ...
# def __rmul__(self, __n: SupportsIndex) -> list[_T]: ...
# def __imul__(self: Self, __n: SupportsIndex) -> Self: ...
# def __contains__(self, __o: object) -> bool: ...
# def __reversed__(self) -> Iterator[_T]: ...
# def __gt__(self, __x: list[_T]) -> bool: ...
# def __ge__(self, __x: list[_T]) -> bool: ...
# def __lt__(self, __x: list[_T]) -> bool: ...
# def __le__(self, __x: list[_T]) -> bool: ...
# if sys.version_info >= (3, 9):
#     def __class_getitem__(cls, __item: Any) -> GenericAlias: ...
