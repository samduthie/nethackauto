"""One step of a game: the new observation and the decision that caused it (None at the start)."""

from dataclasses import dataclass

from nhbot.adapter.observation import Observation
from nhbot.strategy.decision import Decision


@dataclass(frozen=True)
class Step:
    number: int
    observation: Observation
    decision: Decision | None
