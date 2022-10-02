from typing import Any, Dict
from morfosi.registry import Registry
from morfosi.tracing import traceable

from .utils import assert_add, assert_change, assert_delete


class Example:
    def __init__(self) -> None:
        self.nested_dict: Dict[str, Any] = {"foo": "bar"}


def test_tracer_nested_dict_change_property():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    obj.nested_dict["foo"] = "changed"

    assert obj.nested_dict["foo"] == "changed"
    assert_change(registry.changes[0], ["nested_dict", "foo"], "bar", "changed")


def test_tracer_nested_dict_property_multiple_changes():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    obj.nested_dict["foo"] = "changed"
    obj.nested_dict["foo"] = "another"

    assert obj.nested_dict["foo"] == "another"
    assert_change(registry.changes[0], ["nested_dict", "foo"], "bar", "changed")
    assert_change(registry.changes[1], ["nested_dict", "foo"], "changed", "another")


def test_tracer_nested_dict_new_property():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    obj.nested_dict["another"] = "another"

    assert obj.nested_dict["another"] == "another"
    assert_add(registry.changes[0], ["nested_dict", "another"], "another")


def test_tracer_nested_class_delete_property():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    assert "foo" in obj.nested_dict

    del obj.nested_dict["foo"]

    assert "foo" not in obj.nested_dict
    assert_delete(registry.changes[0], ["nested_dict", "foo"], "bar")


def test_tracer_nested_dict_new_nested_property():
    registry = Registry()
    obj = traceable(Example(), registry=registry)

    obj.nested_dict["another"] = {"nested": True}
    obj.nested_dict["another"]["nested"] = False

    assert obj.nested_dict["another"]["nested"] == False
    assert_add(registry.changes[0], ["nested_dict", "another"], {"nested": True})
    assert_change(
        registry.changes[1], ["nested_dict", "another", "nested"], True, False
    )


# TODO: test with the dict.set/get methods? Also remove with pop
