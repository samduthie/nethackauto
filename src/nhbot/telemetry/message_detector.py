"""Gives message for each step that has a message. NLE gives a new message on each step, or none.

In a prompt, the message holds the question. PromptDetector gives that event, not this class.
"""

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event


class MessageDetector:
    def detect(self, previous: Step | None, current: Step) -> list[Event]:
        observation = current.observation
        if not observation.message or observation.input_mode.is_prompt:
            return []
        return [Event.at(current, "message", text=observation.message)]
