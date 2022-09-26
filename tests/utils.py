from typing import Any, List
from morfosi.schema import Change, Add, Delete


def assert_add(add: Add, path: List[str], new_value: Any):
    assert isinstance(add, Add)
    assert add.path == path
    assert add.new_value == new_value
    assert len(add.stack) > 0


def assert_change(change: Change, path: List[str], old_value: Any, new_value: Any):
    assert isinstance(change, Change)
    assert change.path == path
    assert change.old_value == old_value
    assert change.new_value == new_value
    assert len(change.stack) > 0


def assert_delete(delete: Delete, path: List[str], old_value: Any):
    assert isinstance(delete, Delete)
    assert delete.path == path
    assert delete.old_value == old_value
    assert len(delete.stack) > 0
