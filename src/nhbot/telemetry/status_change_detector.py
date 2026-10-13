"""Gives <field>_change when one status value changes, for example hit_points_change."""

from dataclasses import fields

from nhbot.adapter.bottom_line import BottomLine
from nhbot.loop.step import Step
from nhbot.telemetry.event import Event

STATUS_FIELDS = {status_field.name for status_field in fields(BottomLine)}


class StatusChangeDetector:
    def __init__(self, field: str) -> None:
        if field not in STATUS_FIELDS:
            raise ValueError(f"BottomLine has no field {field!r}")
        self._field = field

    def detect(self, previous: Step | None, current: Step) -> list[Event]:
        if previous is None:
            return []
        before = getattr(previous.observation.bottom_line, self._field)
        after = getattr(current.observation.bottom_line, self._field)
        if before == after:
            return []
        return [Event.at(current, f"{self._field}_change", before=before, after=after)]
