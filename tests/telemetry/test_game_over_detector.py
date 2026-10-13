from collections.abc import Callable

from nhbot.loop.step import Step
from nhbot.telemetry.game_over_detector import GameOverDetector


def test_gives_game_over_on_the_last_frame(make_step: Callable[..., Step]) -> None:
    events = GameOverDetector().detect(None, make_step(game_over=True))
    assert [event.kind for event in events] == ["game_over"]


def test_gives_nothing_while_the_game_runs(make_step: Callable[..., Step]) -> None:
    assert GameOverDetector().detect(None, make_step()) == []
