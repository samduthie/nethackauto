"""Finds events in one step.

Input: the previous step (None at the start) and this step. Output: events.
"""

from typing import Protocol

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event


class EventDetector(Protocol):
    def detect(self, previous: Step | None, current: Step) -> list[Event]: ...
