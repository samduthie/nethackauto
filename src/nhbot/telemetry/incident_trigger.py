"""Decides if a step is an incident. Input: a step. Output: the incident name, or None."""

from typing import Protocol

from nhbot.loop.step import Step


class IncidentTrigger(Protocol):
    def check(self, step: Step) -> str | None: ...
