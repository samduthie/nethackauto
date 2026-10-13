"""Shared fixtures: blank observations that each test changes with keyword arguments."""

from collections.abc import Callable
from dataclasses import fields, replace
from typing import Any

import pytest

from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.observation import Observation

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
