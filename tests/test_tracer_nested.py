from morfosi.registry import Registry
from morfosi.tracing import traceable

from .utils import assert_add, assert_change, assert_delete


class Example:
    def __init__(self) -> None:
        self.nested_class = Nested()


class Nested:
    def __init__(self) -> None:
        self.field = "nested"


def test_tracer_nested_class_change_property():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    obj.nested_class.field = "changed"

    assert obj.nested_class.field == "changed"
    assert_change(registry.changes[0], ["nested_class", "field"], "nested", "changed")


def test_tracer_nested_class_property_multiple_changes():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    obj.nested_class.field = "changed"
    obj.nested_class.field = "another"

    assert obj.nested_class.field == "another"
    assert_change(registry.changes[0], ["nested_class", "field"], "nested", "changed")
    assert_change(registry.changes[1], ["nested_class", "field"], "changed", "another")


def test_tracer_nested_class_new_property():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    obj.nested_class.another = "another"  # type: ignore

    assert obj.nested_class.another == "another"  # type: ignore
    assert_add(registry.changes[0], ["nested_class", "another"], "another")


def test_tracer_nested_class_delete_property():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    assert "field" in obj.nested_class.__dict__

    delattr(obj.nested_class, "field")

    assert "field" not in obj.nested_class.__dict__
    assert_delete(registry.changes[0], ["nested_class", "field"], "nested")
