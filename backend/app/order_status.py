"""Order status progression for kitchen tracking.

A linear pipeline — each status has exactly one valid "next" status, plus a
separate terminal "cancelled" state reachable from any non-terminal status.
"""

STATUS_FLOW = ["placed", "confirmed", "preparing", "ready", "out_for_delivery", "delivered"]
TERMINAL_STATUSES = {"delivered", "cancelled"}

ALL_STATUSES = STATUS_FLOW + ["cancelled"]


def next_status(current: str) -> str | None:
    if current not in STATUS_FLOW:
        return None
    idx = STATUS_FLOW.index(current)
    if idx + 1 >= len(STATUS_FLOW):
        return None
    return STATUS_FLOW[idx + 1]


def is_valid_status(status: str) -> bool:
    return status in ALL_STATUSES
