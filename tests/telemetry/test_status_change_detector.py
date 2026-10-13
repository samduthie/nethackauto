from collections.abc import Callable

import pytest

from nhbot.adapter.bottom_line import BottomLine
from nhbot.loop.step import Step
from nhbot.telemetry.status_change_detector import StatusChangeDetector


@pytest.fixture
def hit_points_step(
    make_step: Callable[..., Step], make_bottom_line: Callable[..., BottomLine]
) -> Callable[[int], Step]:
    return lambda hit_points: make_step(bottom_line=make_bottom_line(hit_points=hit_points))


def test_gives_a_change_event(hit_points_step: Callable[[int], Step]) -> None:
    events = StatusChangeDetector("hit_points").detect(hit_points_step(18), hit_points_step(15))
    assert [event.kind for event in events] == ["hit_points_change"]


def test_keeps_the_values_before_and_after(hit_points_step: Callable[[int], Step]) -> None:
    events = StatusChangeDetector("hit_points").detect(hit_points_step(18), hit_points_step(15))
    assert events[0].fields == {"before": 18, "after": 15}


def test_gives_nothing_without_a_change(hit_points_step: Callable[[int], Step]) -> None:
    assert StatusChangeDetector("hit_points").detect(hit_points_step(18), hit_points_step(18)) == []


def test_gives_nothing_on_the_first_step(hit_points_step: Callable[[int], Step]) -> None:
    assert StatusChangeDetector("hit_points").detect(None, hit_points_step(18)) == []


def test_rejects_an_unknown_field() -> None:
    with pytest.raises(ValueError, match="no field"):
        StatusChangeDetector("hitpoints")
