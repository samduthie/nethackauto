"""Gets each Step of the game: the view, the pacing and the telemetry."""

from typing import Protocol

from nhbot.loop.step import Step


class StepListener(Protocol):
    def on_step(self, step: Step) -> None: ...
