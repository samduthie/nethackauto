"""Finds the screen types in one observation: a prompt question, or each sentence of a message.

Normalized text: numbers become "#", choice lists such as "[d or ?*]" become "[...]", and quoted
text (for example an engraving) becomes "...".
"""

import re

from nhbot.adapter.observation import Observation
from nhbot.telemetry.sample_key import SampleKey

SENTENCE_BREAK = re.compile(r" {2,}")  # NetHack puts two spaces between messages; seen in play
CHOICES = re.compile(r"\[[^\]]*\]")
QUOTED = re.compile(r'"[^"]*"')  # an engraving can hold runs of spaces; seen in play
NUMBER = re.compile(r"\d+")


class ScreenClassifier:
    def keys(self, observation: Observation) -> list[SampleKey]:
        mode = observation.input_mode
        if mode.is_prompt:
            # In a prompt, the message holds the question too, so the question is the only key.
            return [SampleKey(mode.name.lower(), self._normalize(observation.screen[0]))]
        sentences = SENTENCE_BREAK.split(self._normalize(observation.message))
        return [SampleKey("message", text) for text in sentences if text]

    @staticmethod
    def _normalize(text: str) -> str:
        return NUMBER.sub("#", CHOICES.sub("[...]", QUOTED.sub('"..."', text.strip())))
