"""Takes each event: the events file, or the buffer for the flight recorder."""

from typing import Protocol

from nhbot.telemetry.event import Event


class EventSink(Protocol):
    def write(self, event: Event) -> None: ...
