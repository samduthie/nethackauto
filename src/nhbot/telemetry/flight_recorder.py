"""Saves one bundle file for each incident, so that the AI can study it.

Incidents come from the triggers, from an exception, or from save(). A bundle holds the last 50
screens, the last events and the state.
"""

import traceback
from collections import deque
from collections.abc import Sequence
from pathlib import Path
from types import TracebackType
from typing import Self

from nhbot.loop.step import Step
from nhbot.telemetry.bundle_format import BundleFormat
from nhbot.telemetry.incident_trigger import IncidentTrigger
from nhbot.telemetry.recent_events import RecentEvents

SCREENS_KEPT = 50  # source: brief section 7.2
MAX_BUNDLES = 10  # stops a flood of bundles in a bad game; source: guess


class FlightRecorder:
    def __init__(
        self,
        directory: Path,
        bundle_format: BundleFormat,
        recent_events: RecentEvents,
        triggers: Sequence[IncidentTrigger],
    ) -> None:
        self._directory = directory
        self._format = bundle_format
        self._recent_events = recent_events
        self._triggers = triggers
        self._steps: deque[Step] = deque(maxlen=SCREENS_KEPT)
        self._bundle_count = 0

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        if exception is not None and not isinstance(exception, KeyboardInterrupt):
            self.save("exception", "".join(traceback.format_exception(exception)))

    def on_step(self, step: Step) -> None:
        self._steps.append(step)
        for trigger in self._triggers:
            incident = trigger.check(step)
            if incident:
                self.save(incident)

    def save(self, incident: str, detail: str = "") -> Path | None:
        if not self._steps or self._bundle_count >= MAX_BUNDLES:
            return None
        self._bundle_count += 1
        path = self._directory / f"bundle-{self._bundle_count:02d}-{incident}.jsonl"
        text = self._format.render(incident, detail, self._steps, self._recent_events.items())
        path.write_text(text, encoding="utf-8")
        return path
