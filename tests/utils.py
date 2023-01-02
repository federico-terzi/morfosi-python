from typing import Any
from morfosi.schema import Action, Change, Add, Delete, Path
from morfosi.tracing.snapshot import snapshot


def assert_add(add: Action, path: Path, new_value: Any):
    assert isinstance(add, Add)
    assert add.path == path
    assert add.new_value == snapshot(new_value)
    assert len(add.stack) > 0


def assert_change(change: Action, path: Path, old_value: Any, new_value: Any):
    assert isinstance(change, Change)
    assert change.path == path
    assert change.old_value == snapshot(old_value)
    assert change.new_value == snapshot(new_value)
    assert len(change.stack) > 0


def assert_delete(delete: Action, path: Path, old_value: Any):
    assert isinstance(delete, Delete)
    assert delete.path == path
    assert delete.old_value == snapshot(old_value)
    assert len(delete.stack) > 0
