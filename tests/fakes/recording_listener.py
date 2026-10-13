"""A StepListener that keeps each step."""

from nhbot.loop.step import Step


class RecordingListener:
    def __init__(self) -> None:
        self.steps: list[Step] = []

    def on_step(self, step: Step) -> None:
        self.steps.append(step)
