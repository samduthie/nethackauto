from collections.abc import Callable

from nhbot.adapter.bottom_line import BottomLine
from nhbot.loop.step import Step
from nhbot.telemetry.event import Event


def test_takes_the_turn_from_the_step(
    make_step: Callable[..., Step], make_bottom_line: Callable[..., BottomLine]
) -> None:
    assert Event.at(make_step(bottom_line=make_bottom_line(turn=9)), "message").turn == 9


def test_takes_the_step_number(make_step: Callable[..., Step]) -> None:
    assert Event.at(make_step(number=12), "message").step == 12


def test_puts_the_fields_at_the_top_level(make_step: Callable[..., Step]) -> None:
    assert Event.at(make_step(), "message", text="Hi").to_dict()["text"] == "Hi"


def test_puts_the_kind_in_the_dict(make_step: Callable[..., Step]) -> None:
    assert Event.at(make_step(), "message").to_dict()["kind"] == "message"
