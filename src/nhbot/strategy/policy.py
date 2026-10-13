"""Chooses the next action. Input: an Observation. Output: a Decision."""

from typing import Protocol

from nhbot.adapter.observation import Observation
from nhbot.strategy.decision import Decision


class Policy(Protocol):
    def decide(self, observation: Observation) -> Decision: ...
