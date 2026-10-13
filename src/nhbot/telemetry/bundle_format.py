"""Writes one bundle as JSON lines: a header, one line for each screen, one line for each event.

A bundle stays below 200 KB: when it is too large, the oldest events go first.
"""

import json
from collections.abc import Sequence
from dataclasses import asdict

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event
from nhbot.telemetry.privacy_filter import PrivacyFilter
from nhbot.telemetry.run_info import RunInfo

MAX_BUNDLE_BYTES = 200_000  # source: brief section 7.2


class BundleFormat:
    def __init__(self, run_info: RunInfo, privacy_filter: PrivacyFilter) -> None:
        self._run_info = run_info
        self._privacy_filter = privacy_filter

    def render(
        self, incident: str, detail: str, steps: Sequence[Step], events: Sequence[Event]
    ) -> str:
        header = self._json(self._header(incident, detail, steps[-1]))
        screens = [self._json(self._screen(step)) for step in steps]
        event_lines = [self._json({"type": "event", **event.to_dict()}) for event in events]
        budget = MAX_BUNDLE_BYTES - len(header) - sum(len(line) + 1 for line in screens)
        while event_lines and sum(len(line) + 1 for line in event_lines) > budget:
            event_lines.pop(0)
        return "\n".join([header, *screens, *event_lines]) + "\n"

    def _header(self, incident: str, detail: str, last_step: Step) -> dict[str, object]:
        observation = last_step.observation
        return {
            "type": "header",
            "incident": incident,
            "detail": self._privacy_filter.clean(detail),
            "run": asdict(self._run_info),
            "step": last_step.number,
            "status": asdict(observation.bottom_line),
            "input_mode": observation.input_mode.name.lower(),
        }

    @staticmethod
    def _screen(step: Step) -> dict[str, object]:
        decision = step.decision
        return {
            "type": "screen",
            "step": step.number,
            "key_pressed": decision.action.key if decision else None,
            "reason": decision.reason if decision else None,
            "lines": [line.rstrip() for line in step.observation.screen],
        }

    @staticmethod
    def _json(content: dict[str, object]) -> str:
        return json.dumps(content)  # ASCII only, so one character is one byte
