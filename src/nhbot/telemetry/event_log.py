"""Turns each step into events and sends each event to each sink. At the end it sends run_end.

The run_end reason is game_over, step_limit, interrupted (ctrl-c) or exception.
"""

from collections.abc import Sequence
from typing import Self

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event
from nhbot.telemetry.event_detector import EventDetector
from nhbot.telemetry.event_sink import EventSink


class EventLog:
    def __init__(self, detectors: Sequence[EventDetector], sinks: Sequence[EventSink]) -> None:
        self._detectors = detectors
        self._sinks = sinks
        self._previous: Step | None = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exception_type: type[BaseException] | None, *exception_info: object) -> None:
        if self._previous is not None:
            reason = self._end_reason(self._previous, exception_type)
            self._send(Event.at(self._previous, "run_end", reason=reason))

    def on_step(self, step: Step) -> None:
        for detector in self._detectors:
            for event in detector.detect(self._previous, step):
                self._send(event)
        self._previous = step

    def _send(self, event: Event) -> None:
        for sink in self._sinks:
            sink.write(event)

    @staticmethod
    def _end_reason(last_step: Step, exception_type: type[BaseException] | None) -> str:
        if exception_type is KeyboardInterrupt:
            return "interrupted"
        if exception_type is not None:
            return "exception"
        return "game_over" if last_step.observation.game_over else "step_limit"
