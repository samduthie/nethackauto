"""Gives game_over on the last frame of a game."""

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event


class GameOverDetector:
    def detect(self, previous: Step | None, current: Step) -> list[Event]:
        return [Event.at(current, "game_over")] if current.observation.game_over else []
