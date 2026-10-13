"""An EventSink that keeps each event."""

from nhbot.telemetry.event import Event


class RecordingSink:
    def __init__(self) -> None:
        self.events: list[Event] = []

    def write(self, event: Event) -> None:
        self.events.append(event)

    def kinds(self) -> list[str]:
        return [event.kind for event in self.events]
