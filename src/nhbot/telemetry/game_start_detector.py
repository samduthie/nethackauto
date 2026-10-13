"""Gives game_start on the first step, with the seed, the character and the code version."""

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event
from nhbot.telemetry.run_info import RunInfo


class GameStartDetector:
    def __init__(self, run_info: RunInfo) -> None:
        self._run_info = run_info

    def detect(self, previous: Step | None, current: Step) -> list[Event]:
        if previous is not None:
            return []
        info = self._run_info
        facts = {"seed": info.seed, "character": info.character, "code_version": info.code_version}
        return [Event.at(current, "game_start", **facts)]
