import json
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from typing import Any

import pytest

from nhbot.loop.step import Step
from nhbot.telemetry.bundle_format import BundleFormat
from nhbot.telemetry.event import Event
from nhbot.telemetry.flight_recorder import MAX_BUNDLES, SCREENS_KEPT, FlightRecorder
from nhbot.telemetry.game_over_trigger import GameOverTrigger
from nhbot.telemetry.privacy_filter import PrivacyFilter
from nhbot.telemetry.recent_events import RecentEvents
from nhbot.telemetry.run_info import RunInfo


@pytest.fixture
def recent_events() -> RecentEvents:
    return RecentEvents(500)


@pytest.fixture
def recorder(tmp_path: Path, run_info: RunInfo, recent_events: RecentEvents) -> FlightRecorder:
    bundle_format = BundleFormat(run_info, PrivacyFilter("/home/alice"))
    return FlightRecorder(tmp_path, bundle_format, recent_events, [GameOverTrigger()])


def bundle_lines(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        raise ValueError("no bundle was saved")
    return [json.loads(line) for line in path.read_text().splitlines()]


def test_saves_a_bundle_when_a_trigger_fires(
    recorder: FlightRecorder, make_step: Callable[..., Step], tmp_path: Path
) -> None:
    recorder.on_step(make_step(game_over=True))
    assert [path.name for path in tmp_path.iterdir()] == ["bundle-01-game_over.jsonl"]


def test_keeps_only_the_last_screens(
    recorder: FlightRecorder, make_step: Callable[..., Step]
) -> None:
    for number in range(SCREENS_KEPT + 10):
        recorder.on_step(make_step(number))
    screens = [line for line in bundle_lines(recorder.save("test")) if line["type"] == "screen"]
    assert len(screens) == SCREENS_KEPT


def test_includes_the_recent_events(
    recorder: FlightRecorder, recent_events: RecentEvents, make_step: Callable[..., Step]
) -> None:
    recent_events.write(Event.at(make_step(), "message", text="It's a wall."))
    recorder.on_step(make_step())
    assert bundle_lines(recorder.save("test"))[-1]["text"] == "It's a wall."


def test_saves_a_bundle_for_an_exception(
    recorder: FlightRecorder, make_step: Callable[..., Step], tmp_path: Path
) -> None:
    with suppress(RuntimeError), recorder:
        recorder.on_step(make_step())
        raise RuntimeError("boom")
    header = bundle_lines(tmp_path / "bundle-01-exception.jsonl")[0]
    assert "RuntimeError: boom" in header["detail"]


def test_saves_nothing_for_ctrl_c(
    recorder: FlightRecorder, make_step: Callable[..., Step], tmp_path: Path
) -> None:
    with suppress(KeyboardInterrupt), recorder:
        recorder.on_step(make_step())
        raise KeyboardInterrupt
    assert list(tmp_path.iterdir()) == []


def test_stops_at_the_bundle_limit(
    recorder: FlightRecorder, make_step: Callable[..., Step], tmp_path: Path
) -> None:
    recorder.on_step(make_step())
    for _ in range(MAX_BUNDLES + 2):
        recorder.save("test")
    assert len(list(tmp_path.iterdir())) == MAX_BUNDLES


def test_saves_nothing_before_the_first_step(recorder: FlightRecorder) -> None:
    assert recorder.save("test") is None
