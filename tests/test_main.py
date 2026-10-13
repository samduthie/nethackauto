"""Seeded games through the whole program. These tests start NLE."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from nhbot.main import main

Play = Callable[[int, int], tuple[str, Path]]


@pytest.fixture
def play(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> Play:
    def run(seed: int, steps: int) -> tuple[str, Path]:
        folders = ["--runs-dir", str(tmp_path / "runs"), "--samples-dir", str(tmp_path / "samples")]
        main(["--seed", str(seed), "--steps", str(steps), *folders])
        return capsys.readouterr().out, max((tmp_path / "runs").iterdir())

    return run


def events(run_directory: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in (run_directory / "events.jsonl").read_text().splitlines()]


def test_prints_the_depth_after_100_steps(play: Play) -> None:
    assert play(1, 100)[0].endswith("after 100 steps, turn 78, max depth 1\n")


def test_same_seed_plays_the_same_game(play: Play) -> None:
    assert play(1, 100)[0].splitlines()[-1] == play(1, 100)[0].splitlines()[-1]


def test_prints_the_run_folder(play: Play) -> None:
    output, run_directory = play(1, 10)
    assert f"run files: {run_directory}" in output


def test_starts_the_events_with_game_start(play: Play) -> None:
    assert events(play(1, 10)[1])[0]["kind"] == "game_start"


def test_ends_the_events_with_the_reason(play: Play) -> None:
    assert events(play(1, 10)[1])[-1]["reason"] == "step_limit"


def test_saves_a_bundle_when_the_hero_dies(play: Play) -> None:
    assert (play(7, 2000)[1] / "bundle-01-game_over.jsonl").exists()  # seed 7 dies at step 1263


def test_saves_samples_of_new_screens(play: Play) -> None:
    run_directory = play(1, 100)[1]
    assert any((run_directory.parent.parent / "samples").iterdir())


def test_prints_the_number_of_new_samples(play: Play) -> None:
    assert "new samples: " in play(1, 10)[0]
