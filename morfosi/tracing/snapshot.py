from typing import Any

from morfosi.schema import ValueSnapshotStrategy


def snapshot(
    value: Any,
    value_snapshot_strategy: ValueSnapshotStrategy = ValueSnapshotStrategy.STRING,
) -> Any:
    if value_snapshot_strategy == ValueSnapshotStrategy.STRING:
        return string_snapshot(value)

    raise Exception(f"invalid value_snapshot_strategy: {value_snapshot_strategy}")


def string_snapshot(value: Any) -> str:
    return str(value)
