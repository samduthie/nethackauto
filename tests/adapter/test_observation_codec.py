import json
from collections.abc import Callable

import pytest

from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.observation import Observation
from nhbot.adapter.observation_codec import ObservationCodec


@pytest.fixture
def observation(
    make_observation: Callable[..., Observation], make_bottom_line: Callable[..., BottomLine]
) -> Observation:
    return make_observation(
        screen=("What do you want to eat? [d or ?*]".ljust(80),) + (" " * 80,) * 23,
        colors=(bytes(range(16)) * 5,) * 24,
        cursor=(0, 35),
        glyphs=((2359,) * 79,) * 21,
        message="What do you want to eat? [d or ?*] ",
        bottom_line=make_bottom_line(depth=1, turn=12, hit_points=18),
        input_mode=InputMode.KEY_PROMPT,
    )


def test_gives_back_the_same_observation_after_json(observation: Observation) -> None:
    codec = ObservationCodec()
    assert codec.decode(json.loads(json.dumps(codec.encode(observation)))) == observation


def test_writes_colors_as_hex(observation: Observation) -> None:
    assert ObservationCodec().encode(observation)["colors"][0].startswith("000102")


def test_writes_one_text_line_for_each_glyph_row(observation: Observation) -> None:
    assert ObservationCodec().encode(observation)["glyphs"][0].startswith("2359 2359")
