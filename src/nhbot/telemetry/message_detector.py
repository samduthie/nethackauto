"""Gives message for each step that has a message. NLE gives a new message on each step, or none."""

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event


class MessageDetector:
    def detect(self, previous: Step | None, current: Step) -> list[Event]:
        message = current.observation.message
        return [Event.at(current, "message", text=message)] if message else []
