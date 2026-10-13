"""An EventDetector that gives one "seen" event for each step. It keeps each previous step."""

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event


class RecordingDetector:
    def __init__(self) -> None:
        self.previous_steps: list[Step | None] = []

    def detect(self, previous: Step | None, current: Step) -> list[Event]:
        self.previous_steps.append(previous)
        return [Event.at(current, "seen")]
