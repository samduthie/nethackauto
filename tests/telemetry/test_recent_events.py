from collections.abc import Callable

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event
from nhbot.telemetry.recent_events import RecentEvents


def test_keeps_only_the_last_events_oldest_first(make_step: Callable[..., Step]) -> None:
    recent = RecentEvents(2)
    for kind in ("first", "second", "third"):
        recent.write(Event.at(make_step(), kind))
    assert [event.kind for event in recent.items()] == ["second", "third"]
