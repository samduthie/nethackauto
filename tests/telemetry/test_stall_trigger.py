from collections.abc import Callable

import pytest

from nhbot.adapter.bottom_line import BottomLine
from nhbot.loop.step import Step
from nhbot.telemetry.stall_trigger import StallTrigger


@pytest.fixture
def results(
    make_step: Callable[..., Step], make_bottom_line: Callable[..., BottomLine]
) -> Callable[[list[int]], list[str | None]]:
    def check_turns(turns: list[int]) -> list[str | None]:
        trigger = StallTrigger(limit=2)
        return [trigger.check(make_step(bottom_line=make_bottom_line(turn=turn))) for turn in turns]

    return check_turns


def test_fires_when_the_turn_stays_the_same(
    results: Callable[[list[int]], list[str | None]],
) -> None:
    assert results([5, 5, 5]) == [None, None, "stalled"]


def test_fires_one_time_for_each_stall(results: Callable[[list[int]], list[str | None]]) -> None:
    assert results([5, 5, 5, 5, 5]).count("stalled") == 1


def test_starts_again_when_time_passes(results: Callable[[list[int]], list[str | None]]) -> None:
    assert results([5, 5, 6, 6, 6]) == [None, None, None, None, "stalled"]
