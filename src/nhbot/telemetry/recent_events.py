"""Keeps the last events for the flight recorder. Input: events. Output: items(), oldest first."""

from collections import deque

from nhbot.telemetry.event import Event


class RecentEvents:
    def __init__(self, capacity: int) -> None:
        self._events: deque[Event] = deque(maxlen=capacity)

    def write(self, event: Event) -> None:
        self._events.append(event)

    def items(self) -> tuple[Event, ...]:
        return tuple(self._events)
