from morfosi.registry import Registry
from morfosi.tracer import Tracer

from .utils import assert_add, assert_change, assert_delete


class Example:
    def __init__(self) -> None:
        self.prop = "value"


def test_tracer_class_property_value_change():
    registry = Registry()
    obj = Tracer(Example(), registry=registry)

    obj.prop = "changed"

    assert obj.prop == "changed"
    assert_change(registry.changes[0], ["prop"], "value", "changed")


def test_tracer_class_property_multiple_changes():
    registry = Registry()
    obj = Tracer(Example(), registry=registry)

    obj.prop = "changed"
    obj.prop = "another"

    assert obj.prop == "another"
    assert_change(registry.changes[0], ["prop"], "value", "changed")
    assert_change(registry.changes[1], ["prop"], "changed", "another")


def test_tracer_class_new_property():
    registry = Registry()
    obj = Tracer(Example(), registry=registry)

    obj.another = "another"

    assert obj.another == "another"
    assert_add(registry.changes[0], ["another"], "another")


def test_tracer_class_delete_property():
    registry = Registry()
    obj = Tracer(Example(), registry=registry)

    assert "prop" in obj.__dict__

    delattr(obj, "prop")

    assert "prop" not in obj.__dict__
    assert_delete(registry.changes[0], ["prop"], "value")
