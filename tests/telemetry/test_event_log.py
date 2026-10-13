from collections.abc import Callable
from contextlib import suppress

import pytest
from fakes.recording_detector import RecordingDetector
from fakes.recording_sink import RecordingSink

from nhbot.loop.step import Step
from nhbot.telemetry.event_log import EventLog

END_CASES = [
    (None, False, "step_limit"),
    (None, True, "game_over"),
    (KeyboardInterrupt, False, "interrupted"),
    (RuntimeError, False, "exception"),
]


def test_sends_each_event_to_each_sink(make_step: Callable[..., Step]) -> None:
    second_sink = RecordingSink()
    EventLog([RecordingDetector()], [RecordingSink(), second_sink]).on_step(make_step())
    assert second_sink.kinds() == ["seen"]


def test_gives_the_previous_step_to_the_detectors(make_step: Callable[..., Step]) -> None:
    detector = RecordingDetector()
    event_log = EventLog([detector], [])
    first_step = make_step(0)
    event_log.on_step(first_step)
    event_log.on_step(make_step(1))
    assert detector.previous_steps == [None, first_step]


@pytest.mark.parametrize(("exception_type", "game_over", "reason"), END_CASES)
def test_ends_with_the_reason(
    make_step: Callable[..., Step],
    exception_type: type[BaseException] | None,
    game_over: bool,
    reason: str,
) -> None:
    sink = RecordingSink()
    with suppress(BaseException), EventLog([], [sink]) as log:
        log.on_step(make_step(game_over=game_over))
        if exception_type:
            raise exception_type
    assert sink.events[-1].fields["reason"] == reason


def test_sends_nothing_at_the_end_without_steps() -> None:
    sink = RecordingSink()
    with EventLog([], [sink]):
        pass
    assert sink.events == []
