from pathlib import Path

from nhbot.run_options import RunOptions


def test_default_character_is_a_dwarvish_valkyrie() -> None:
    assert RunOptions.parse([]).character == "val-dwa-law-fem"


def test_reads_the_seed() -> None:
    assert RunOptions.parse(["--seed", "9"]).seed == 9


def test_steps_sets_the_step_limit() -> None:
    assert RunOptions.parse(["--steps", "100"]).max_steps == 100


def test_watch_is_off_by_default() -> None:
    assert not RunOptions.parse([]).watch


def test_runs_folder_is_runs_by_default() -> None:
    assert RunOptions.parse([]).runs_directory == Path("runs")


def test_reads_the_runs_folder() -> None:
    assert RunOptions.parse(["--runs-dir", "/tmp/runs"]).runs_directory == Path("/tmp/runs")


def test_samples_folder_is_samples_by_default() -> None:
    assert RunOptions.parse([]).samples_directory == Path("samples")
