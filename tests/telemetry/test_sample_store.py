import json
from pathlib import Path

from nhbot.telemetry.sample_key import SampleKey
from nhbot.telemetry.sample_store import SampleStore

KEY = SampleKey("message", "It's a wall.")


def test_has_no_sample_at_first(tmp_path: Path) -> None:
    assert not SampleStore(tmp_path / "samples").has(KEY)


def test_has_a_sample_after_it_saves_one(tmp_path: Path) -> None:
    store = SampleStore(tmp_path / "samples")
    store.save(KEY, {"text": KEY.text})
    assert store.has(KEY)


def test_writes_the_content_as_json(tmp_path: Path) -> None:
    path = SampleStore(tmp_path / "samples").save(KEY, {"text": KEY.text})
    assert json.loads(path.read_text())["text"] == "It's a wall."
