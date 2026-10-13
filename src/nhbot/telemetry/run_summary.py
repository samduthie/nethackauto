"""Sums up one game in one line. Input: each Step. Output: line()."""

from nhbot.loop.step import Step


class RunSummary:
    def __init__(self, seed: int) -> None:
        self._seed = seed
        self._steps = 0
        self._turn = 0
        self._max_depth = 0
        self._game_over = False

    def on_step(self, step: Step) -> None:
        bottom_line = step.observation.bottom_line
        self._steps = step.number
        self._turn = max(self._turn, bottom_line.turn)  # NLE sets the stats to 0 on the end screens
        self._max_depth = max(self._max_depth, bottom_line.depth)
        self._game_over = step.observation.game_over

    def line(self) -> str:
        end = "game over" if self._game_over else "stopped"
        return (
            f"seed {self._seed}: {end} after {self._steps} steps, "
            f"turn {self._turn}, max depth {self._max_depth}"
        )
