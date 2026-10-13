from collections.abc import Callable

from nhbot.adapter.input_mode import InputMode
from nhbot.loop.step import Step
from nhbot.telemetry.message_detector import MessageDetector


def test_gives_a_message_event(make_step: Callable[..., Step]) -> None:
    events = MessageDetector().detect(None, make_step(message="It's a wall."))
    assert [event.kind for event in events] == ["message"]


def test_keeps_the_text(make_step: Callable[..., Step]) -> None:
    events = MessageDetector().detect(None, make_step(message="It's a wall."))
    assert events[0].fields["text"] == "It's a wall."


def test_gives_nothing_without_a_message(make_step: Callable[..., Step]) -> None:
    assert MessageDetector().detect(None, make_step()) == []


def test_gives_nothing_for_a_prompt(make_step: Callable[..., Step]) -> None:
    step = make_step(message="What do you want to eat? [d or ?*] ", input_mode=InputMode.KEY_PROMPT)
    assert MessageDetector().detect(None, step) == []
