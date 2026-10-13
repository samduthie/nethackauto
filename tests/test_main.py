"""Seeded games through the whole program. These tests start NLE."""

import pytest

from nhbot.main import main

HUNDRED_STEPS = ["--seed", "1", "--steps", "100"]


def test_prints_the_depth_after_100_steps(capsys: pytest.CaptureFixture[str]) -> None:
    main(HUNDRED_STEPS)
    assert capsys.readouterr().out.endswith("after 100 steps, turn 78, max depth 1\n")


def test_same_seed_plays_the_same_game(capsys: pytest.CaptureFixture[str]) -> None:
    main(HUNDRED_STEPS)
    first_game = capsys.readouterr().out
    main(HUNDRED_STEPS)
    assert capsys.readouterr().out == first_game
