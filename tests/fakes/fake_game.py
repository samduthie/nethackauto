"""A Game that plays back a list of observations and records the actions that it gets."""

from nhbot.adapter.action import Action
from nhbot.adapter.observation import Observation


class FakeGame:
    def __init__(self, observations: list[Observation]) -> None:
        self.observations = observations
        self.actions: list[Action] = []

    def start(self) -> Observation:
        return self.observations[0]

    def send(self, action: Action) -> Observation:
        self.actions.append(action)
        return self.observations[min(len(self.actions), len(self.observations) - 1)]
