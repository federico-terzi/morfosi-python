from typing import Any

PRIMITIVE_TYPES = (int, str, bool, float)


def is_primitive(obj: Any) -> bool:
    if obj is None:
        return True
    return type(obj) in PRIMITIVE_TYPES


def is_morfosi_builtin(field_name: str) -> bool:
    return field_name.startswith("_self_tracer_")
