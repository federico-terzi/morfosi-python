from typing import List, Optional, TypeVar, cast

from morfosi.registry import Registry
from morfosi.schema import Path
from morfosi.tracing.class_tracer import ClassTracer
from morfosi.tracing.utils import is_primitive

T = TypeVar("T")


def traceable(obj: T, registry: Optional[Registry] = None, path: Path = []) -> T:
    if isinstance(obj, list):
        # TODO
        pass
    elif isinstance(obj, dict):
        # TODO
        pass
    elif not is_primitive(obj):
        return cast(T, ClassTracer(obj, registry=registry, path=path))
    else:
        return obj