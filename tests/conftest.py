"""Shared fixtures: blank observations and steps that each test changes with keyword arguments."""

from collections.abc import Callable
from dataclasses import fields, replace
from typing import Any

import pytest

from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.observation import Observation
from nhbot.loop.step import Step
from nhbot.strategy.decision import Decision
from nhbot.telemetry.run_info import RunInfo

BLANK_BOTTOM_LINE = BottomLine(*[0] * len(fields(BottomLine)))
BLANK_OBSERVATION = Observation(
    screen=(" " * 80,) * 24,
    colors=(bytes(80),) * 24,
    cursor=(0, 0),
    glyphs=(),
    message="",
    bottom_line=BLANK_BOTTOM_LINE,
    input_mode=InputMode.COMMAND,
    game_over=False,
)


@pytest.fixture
def make_bottom_line() -> Callable[..., BottomLine]:
    return lambda **changes: replace(BLANK_BOTTOM_LINE, **changes)


@pytest.fixture
def make_observation() -> Callable[..., Observation]:
    def make(**changes: Any) -> Observation:
        return replace(BLANK_OBSERVATION, **changes)

    return make


@pytest.fixture
def make_step() -> Callable[..., Step]:
    def make(number: int = 0, decision: Decision | None = None, **changes: Any) -> Step:
        return Step(number, replace(BLANK_OBSERVATION, **changes), decision)

    return make


@pytest.fixture
def run_info() -> RunInfo:
    return RunInfo("20261013-120000-seed4", 4, "val-dwa-law-fem", "abc1234")
