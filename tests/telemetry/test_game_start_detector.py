from collections.abc import Callable

from nhbot.loop.step import Step
from nhbot.telemetry.game_start_detector import GameStartDetector
from nhbot.telemetry.run_info import RunInfo


def test_gives_game_start_on_the_first_step(
    make_step: Callable[..., Step], run_info: RunInfo
) -> None:
    assert [event.kind for event in GameStartDetector(run_info).detect(None, make_step())] == [
        "game_start"
    ]


def test_includes_the_seed(make_step: Callable[..., Step], run_info: RunInfo) -> None:
    assert GameStartDetector(run_info).detect(None, make_step())[0].fields["seed"] == 4


def test_includes_the_code_version(make_step: Callable[..., Step], run_info: RunInfo) -> None:
    event = GameStartDetector(run_info).detect(None, make_step())[0]
    assert event.fields["code_version"] == "abc1234"


def test_gives_nothing_later(make_step: Callable[..., Step], run_info: RunInfo) -> None:
    assert GameStartDetector(run_info).detect(make_step(), make_step(1)) == []
