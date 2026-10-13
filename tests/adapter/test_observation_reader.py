from typing import Any

import numpy as np
import pytest
from nle import nethack
from numpy.typing import NDArray

from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.observation import Observation
from nhbot.adapter.observation_reader import ObservationReader

BOTTOM_LINE_INDEXES = [
    ("x", nethack.NLE_BL_X),
    ("y", nethack.NLE_BL_Y),
    ("strength", nethack.NLE_BL_STR25),
    ("strength_with_percentile", nethack.NLE_BL_STR125),
    ("dexterity", nethack.NLE_BL_DEX),
    ("constitution", nethack.NLE_BL_CON),
    ("intelligence", nethack.NLE_BL_INT),
    ("wisdom", nethack.NLE_BL_WIS),
    ("charisma", nethack.NLE_BL_CHA),
    ("score", nethack.NLE_BL_SCORE),
    ("hit_points", nethack.NLE_BL_HP),
    ("max_hit_points", nethack.NLE_BL_HPMAX),
    ("depth", nethack.NLE_BL_DEPTH),
    ("gold", nethack.NLE_BL_GOLD),
    ("energy", nethack.NLE_BL_ENE),
    ("max_energy", nethack.NLE_BL_ENEMAX),
    ("armor_class", nethack.NLE_BL_AC),
    ("monster_level", nethack.NLE_BL_HD),
    ("experience_level", nethack.NLE_BL_XP),
    ("experience_points", nethack.NLE_BL_EXP),
    ("turn", nethack.NLE_BL_TIME),
    ("hunger_state", nethack.NLE_BL_HUNGER),
    ("carrying_capacity", nethack.NLE_BL_CAP),
    ("dungeon_number", nethack.NLE_BL_DNUM),
    ("level_number", nethack.NLE_BL_DLEVEL),
    ("conditions", nethack.NLE_BL_CONDITION),
    ("alignment", nethack.NLE_BL_ALIGN),
]
INPUT_MODES = [
    ([0, 0, 0], InputMode.COMMAND),
    ([0, 0, 1], InputMode.MORE),
    ([1, 0, 0], InputMode.KEY_PROMPT),
    ([0, 1, 0], InputMode.TEXT_PROMPT),
    ([0, 1, 1], InputMode.MORE),  # seen in play: "--More--" before the engrave text prompt
]


@pytest.fixture
def nle_observation() -> dict[str, NDArray[Any]]:
    screen = np.full((24, 80), ord(" "), dtype=np.uint8)
    screen[0, :5] = list(b"Hello")
    colors = np.zeros((24, 80), dtype=np.int8)
    colors[3, 4] = 1
    message = np.zeros(256, dtype=np.uint8)
    message[:5] = list(b"Hello")
    return {
        "tty_chars": screen,
        "tty_colors": colors,
        "tty_cursor": np.array([16, 66], dtype=np.uint8),
        "glyphs": np.full((21, 79), 2359, dtype=np.int16),
        "message": message,
        "blstats": np.arange(27, dtype=np.int64),  # each value is its own index
        "misc": np.zeros(3, dtype=np.int32),
    }


@pytest.fixture
def observation(nle_observation: dict[str, NDArray[Any]]) -> Observation:
    return ObservationReader().read(nle_observation, game_over=False)


def test_reads_the_screen_text(observation: Observation) -> None:
    assert observation.screen[0].startswith("Hello")


def test_reads_the_colors(observation: Observation) -> None:
    assert observation.colors[3][4] == 1


def test_reads_the_cursor(observation: Observation) -> None:
    assert observation.cursor == (16, 66)


def test_reads_the_glyphs(observation: Observation) -> None:
    assert observation.glyphs[20][78] == 2359


def test_removes_the_message_padding(observation: Observation) -> None:
    assert observation.message == "Hello"


@pytest.mark.parametrize(("field", "index"), BOTTOM_LINE_INDEXES)
def test_maps_each_status_value(observation: Observation, field: str, index: int) -> None:
    assert getattr(observation.bottom_line, field) == index


@pytest.mark.parametrize(("misc", "input_mode"), INPUT_MODES)
def test_finds_the_input_mode(
    nle_observation: dict[str, NDArray[Any]], misc: list[int], input_mode: InputMode
) -> None:
    nle_observation["misc"] = np.array(misc, dtype=np.int32)
    assert ObservationReader().read(nle_observation, game_over=False).input_mode is input_mode


def test_keeps_game_over(nle_observation: dict[str, NDArray[Any]]) -> None:
    assert ObservationReader().read(nle_observation, game_over=True).game_over
