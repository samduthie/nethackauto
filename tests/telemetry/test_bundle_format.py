import json
from collections.abc import Callable
from typing import Any

import pytest

from nhbot.adapter.action import Action
from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.key import Key
from nhbot.loop.step import Step
from nhbot.strategy.decision import Decision
from nhbot.telemetry.bundle_format import MAX_BUNDLE_BYTES, BundleFormat
from nhbot.telemetry.event import Event
from nhbot.telemetry.privacy_filter import PrivacyFilter
from nhbot.telemetry.run_info import RunInfo

FULL_SCREEN = ("#" * 80,) * 24
LONG_MESSAGE = "The fox bites! " * 17  # NLE messages can have 256 characters


@pytest.fixture
def render(run_info: RunInfo) -> Callable[..., list[dict[str, Any]]]:
    def rendered(steps: list[Step], events: list[Event], detail: str = "") -> list[dict[str, Any]]:
        bundle_format = BundleFormat(run_info, PrivacyFilter("/home/alice"))
        text = bundle_format.render("game_over", detail, steps, events)
        return [json.loads(line) for line in text.splitlines()]

    return rendered


@pytest.fixture
def full_bundle_bytes(run_info: RunInfo, make_step: Callable[..., Step]) -> int:
    steps = [make_step(number, screen=FULL_SCREEN) for number in range(50)]
    events = [Event.at(steps[-1], "message", text=LONG_MESSAGE) for _ in range(500)]
    text = BundleFormat(run_info, PrivacyFilter("/home/alice")).render(
        "game_over", "", steps, events
    )
    return len(text.encode())


def test_puts_one_line_for_each_screen_and_event(
    render: Callable[..., list[dict[str, Any]]], make_step: Callable[..., Step]
) -> None:
    lines = render([make_step(0), make_step(1)], [Event.at(make_step(), "message")])
    assert [line["type"] for line in lines] == ["header", "screen", "screen", "event"]


def test_header_names_the_incident(
    render: Callable[..., list[dict[str, Any]]], make_step: Callable[..., Step]
) -> None:
    assert render([make_step()], [])[0]["incident"] == "game_over"


def test_header_has_the_seed(
    render: Callable[..., list[dict[str, Any]]], make_step: Callable[..., Step]
) -> None:
    assert render([make_step()], [])[0]["run"]["seed"] == 4


def test_header_has_the_last_status(
    render: Callable[..., list[dict[str, Any]]],
    make_step: Callable[..., Step],
    make_bottom_line: Callable[..., BottomLine],
) -> None:
    steps = [make_step(0), make_step(1, bottom_line=make_bottom_line(depth=3))]
    assert render(steps, [])[0]["status"]["depth"] == 3


def test_cleans_the_detail(
    render: Callable[..., list[dict[str, Any]]], make_step: Callable[..., Step]
) -> None:
    assert render([make_step()], [], "/home/alice/main.py")[0]["detail"] == "~/main.py"


def test_cuts_spaces_at_the_end_of_screen_lines(
    render: Callable[..., list[dict[str, Any]]], make_step: Callable[..., Step]
) -> None:
    assert render([make_step()], [])[1]["lines"][0] == ""


def test_keeps_the_key_pressed(
    render: Callable[..., list[dict[str, Any]]], make_step: Callable[..., Step]
) -> None:
    step = make_step(1, Decision(Action(Key.ENTER), "continue after --More--"))
    assert render([step], [])[1]["key_pressed"] == "\r"


def test_stays_below_the_size_limit(full_bundle_bytes: int) -> None:
    assert full_bundle_bytes <= MAX_BUNDLE_BYTES


def test_drops_the_oldest_events_when_too_large(
    render: Callable[..., list[dict[str, Any]]], make_step: Callable[..., Step]
) -> None:
    steps = [make_step(number, screen=FULL_SCREEN) for number in range(50)]
    events = [Event.at(make_step(number), "message", text=LONG_MESSAGE) for number in range(500)]
    assert len([line for line in render(steps, events) if line["type"] == "event"]) < 500


def test_keeps_the_newest_events_when_it_cuts(
    render: Callable[..., list[dict[str, Any]]], make_step: Callable[..., Step]
) -> None:
    steps = [make_step(number, screen=FULL_SCREEN) for number in range(50)]
    events = [Event.at(make_step(number), "message", text=LONG_MESSAGE) for number in range(500)]
    assert render(steps, events)[-1]["step"] == 499
