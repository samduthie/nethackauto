"""Fires on the game-over frame."""

from nhbot.loop.step import Step


class GameOverTrigger:
    def check(self, step: Step) -> str | None:
        return "game_over" if step.observation.game_over else None
