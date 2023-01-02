from morfosi.registry import Registry
from morfosi.tracing import traceable

from .utils import assert_add, assert_change, assert_delete


def test_tracer_list_value_change():
    registry = Registry()
    example_list = [1, 2, 3]
    traceable_list = traceable(example_list, registry=registry)

    traceable_list[0] = 4
    traceable_list[1] = 5

    assert traceable_list[0] == 4
    assert traceable_list[1] == 5
    assert traceable_list[2] == 3
    assert traceable_list == [4, 5, 3]
    assert_change(registry.changes[0], [0], 1, 4)
    assert_change(registry.changes[1], [1], 2, 5)


def test_tracer_list_add_value():
    registry = Registry()
    example_list = [1, 2, 3]
    traceable_list = traceable(example_list, registry=registry)

    traceable_list.append(4)
    traceable_list.append(5)

    assert len(traceable_list) == 5
    assert traceable_list == [1, 2, 3, 4, 5]
    assert_add(registry.changes[0], [3], 4)
    assert_add(registry.changes[1], [4], 5)


# TODO: test with slices, and all the list operations

# def test_tracer_class_property_multiple_changes():
#     registry = Registry()
#     obj = traceable(Example(), registry=registry)

#     obj.prop = "changed"
#     obj.prop = "another"

#     assert obj.prop == "another"
#     assert_change(registry.changes[0], ["prop"], "value", "changed")
#     assert_change(registry.changes[1], ["prop"], "changed", "another")


# def test_tracer_class_new_property():
#     registry = Registry()
#     obj = traceable(Example(), registry=registry)

#     obj.another = "another"  # type: ignore

#     assert obj.another == "another"  # type: ignore
#     assert_add(registry.changes[0], ["another"], "another")


# def test_tracer_class_delete_property():
#     registry = Registry()
#     obj = traceable(Example(), registry=registry)

#     assert "prop" in obj.__dict__

#     delattr(obj, "prop")

#     assert "prop" not in obj.__dict__
#     assert_delete(registry.changes[0], ["prop"], "value")
