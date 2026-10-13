"""Fires when the game turn stays the same for many steps: the bot sends keys that use no time.

It fires one time for each stall.
"""

from nhbot.loop.step import Step

STALL_LIMIT = 100  # steps with no new turn; source: guess


class StallTrigger:
    def __init__(self, limit: int = STALL_LIMIT) -> None:
        self._limit = limit
        self._turn = -1
        self._steps_without_time = 0

    def check(self, step: Step) -> str | None:
        turn = step.observation.bottom_line.turn
        if turn != self._turn:
            self._turn, self._steps_without_time = turn, 0
            return None
        self._steps_without_time += 1
        return "stalled" if self._steps_without_time == self._limit else None
