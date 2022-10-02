from morfosi.registry import Registry
from morfosi.tracing import traceable

from .utils import assert_add, assert_change, assert_delete


class Example:
    def __init__(self) -> None:
        self.nested_class = Nested()


class Nested:
    def __init__(self) -> None:
        self.field = "nested"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Nested):
            return False
        return self.field == __o.field


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


def test_tracer_nested_class_new_nested_property():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    obj.another_nested = Nested()  # type: ignore
    obj.another_nested.field = "changed"  # type: ignore

    assert obj.another_nested.field == "changed"  # type: ignore
    assert_add(registry.changes[0], ["another_nested"], Nested())
    assert_change(registry.changes[1], ["another_nested", "field"], "nested", "changed")
