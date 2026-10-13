"""A Policy that always gives the same decision."""

from nhbot.adapter.observation import Observation
from nhbot.strategy.decision import Decision


class FixedPolicy:
    def __init__(self, decision: Decision) -> None:
        self.decision = decision

    def decide(self, observation: Observation) -> Decision:
        return self.decision
