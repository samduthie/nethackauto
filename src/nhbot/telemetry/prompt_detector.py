"""Gives prompt when the game asks a new question. The text is the top line of the screen."""

from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.observation import Observation
from nhbot.loop.step import Step
from nhbot.telemetry.event import Event

PROMPT_MODES = {InputMode.KEY_PROMPT, InputMode.TEXT_PROMPT}


class PromptDetector:
    def detect(self, previous: Step | None, current: Step) -> list[Event]:
        observation = current.observation
        if observation.input_mode not in PROMPT_MODES:
            return []
        if previous and self._question(previous.observation) == self._question(observation):
            return []
        mode = observation.input_mode.name.lower()
        return [Event.at(current, "prompt", mode=mode, text=observation.screen[0].strip())]

    @staticmethod
    def _question(observation: Observation) -> tuple[InputMode, str]:
        return observation.input_mode, observation.screen[0].strip()
