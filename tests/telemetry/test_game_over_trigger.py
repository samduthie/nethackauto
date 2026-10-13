from collections.abc import Callable

from nhbot.loop.step import Step
from nhbot.telemetry.game_over_trigger import GameOverTrigger


def test_fires_on_game_over(make_step: Callable[..., Step]) -> None:
    assert GameOverTrigger().check(make_step(game_over=True)) == "game_over"


def test_stays_quiet_while_the_game_runs(make_step: Callable[..., Step]) -> None:
    assert GameOverTrigger().check(make_step()) is None
