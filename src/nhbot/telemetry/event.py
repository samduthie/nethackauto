"""One thing that happened in the game, with when and where.

Input: a Step. Output: a flat dict for JSON.
"""

from dataclasses import dataclass, field
from typing import Self

from nhbot.loop.step import Step


@dataclass(frozen=True)
class Event:
    kind: str
    step: int
    turn: int
    depth: int
    x: int
    y: int
    fields: dict[str, object] = field(default_factory=dict)

    @classmethod
    def at(cls, step: Step, kind: str, **fields: object) -> Self:
        status = step.observation.bottom_line
        return cls(kind, step.number, status.turn, status.depth, status.x, status.y, fields)

    def to_dict(self) -> dict[str, object]:
        place = {
            "step": self.step,
            "turn": self.turn,
            "depth": self.depth,
            "x": self.x,
            "y": self.y,
        }
        return {**place, "kind": self.kind, **self.fields}
