import json
from collections.abc import Callable
from pathlib import Path

import pytest

from nhbot.adapter.observation_codec import ObservationCodec
from nhbot.loop.step import Step
from nhbot.telemetry.run_info import RunInfo
from nhbot.telemetry.sample_collector import SampleCollector
from nhbot.telemetry.sample_store import SampleStore
from nhbot.telemetry.screen_classifier import ScreenClassifier


@pytest.fixture
def collector(tmp_path: Path, run_info: RunInfo) -> SampleCollector:
    store = SampleStore(tmp_path / "samples")
    return SampleCollector(ScreenClassifier(), store, ObservationCodec(), run_info)


def test_saves_a_sample_of_a_new_message(
    collector: SampleCollector, make_step: Callable[..., Step], tmp_path: Path
) -> None:
    collector.on_step(make_step(message="It's a wall."))
    assert len(list((tmp_path / "samples").iterdir())) == 1


def test_saves_each_screen_type_once(
    collector: SampleCollector, make_step: Callable[..., Step]
) -> None:
    collector.on_step(make_step(message="The fox bites!  The fox bites!"))
    collector.on_step(make_step(1, message="The fox bites!"))
    assert collector.saved_count == 1


def test_saves_the_observation_for_a_golden_file(
    collector: SampleCollector, make_step: Callable[..., Step], tmp_path: Path
) -> None:
    step = make_step(message="It's a wall.")
    collector.on_step(step)
    content = json.loads(next((tmp_path / "samples").iterdir()).read_text())
    assert ObservationCodec().decode(content["observation"]) == step.observation
