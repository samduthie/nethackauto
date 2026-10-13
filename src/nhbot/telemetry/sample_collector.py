"""Saves one sample of each new screen type (shadow mode). Input: steps. Output: sample files.

A sample holds the key, the run facts, the step and the whole observation, so that it can become
a golden file for a parser test.
"""

from dataclasses import asdict

from nhbot.adapter.observation_codec import ObservationCodec
from nhbot.loop.step import Step
from nhbot.telemetry.run_info import RunInfo
from nhbot.telemetry.sample_key import SampleKey
from nhbot.telemetry.sample_store import SampleStore
from nhbot.telemetry.screen_classifier import ScreenClassifier


class SampleCollector:
    def __init__(
        self,
        classifier: ScreenClassifier,
        store: SampleStore,
        codec: ObservationCodec,
        run_info: RunInfo,
    ) -> None:
        self._classifier = classifier
        self._store = store
        self._codec = codec
        self._run_info = run_info
        self._saved_count = 0

    @property
    def saved_count(self) -> int:
        return self._saved_count

    def on_step(self, step: Step) -> None:
        for key in self._classifier.keys(step.observation):
            if not self._store.has(key):
                self._store.save(key, self._content(key, step))
                self._saved_count += 1

    def _content(self, key: SampleKey, step: Step) -> dict[str, object]:
        return {
            "kind": key.kind,
            "text": key.text,
            "run": asdict(self._run_info),
            "step": step.number,
            "observation": self._codec.encode(step.observation),
        }
