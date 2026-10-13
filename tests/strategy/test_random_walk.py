import random
from collections.abc import Callable

import pytest

from nhbot.adapter.action import Action
from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.key import Key
from nhbot.adapter.observation import Observation
from nhbot.strategy.random_walk import SAFE_KEYS, RandomWalk


def keys_of(seed: int, observation: Observation) -> list[str]:
    walk = RandomWalk(random.Random(seed))
    return [walk.decide(observation).action.key for _ in range(20)]


def test_continues_after_more(make_observation: Callable[..., Observation]) -> None:
    observation = make_observation(input_mode=InputMode.MORE)
    assert RandomWalk(random.Random(1)).decide(observation).action == Action(Key.ENTER)


@pytest.mark.parametrize("input_mode", [InputMode.KEY_PROMPT, InputMode.TEXT_PROMPT])
def test_declines_a_prompt(
    make_observation: Callable[..., Observation], input_mode: InputMode
) -> None:
    observation = make_observation(input_mode=input_mode)
    assert RandomWalk(random.Random(1)).decide(observation).action == Action(Key.ESCAPE)


def test_uses_only_safe_keys(make_observation: Callable[..., Observation]) -> None:
    assert set(keys_of(1, make_observation())) <= set(SAFE_KEYS)


def test_same_seed_gives_the_same_keys(make_observation: Callable[..., Observation]) -> None:
    assert keys_of(5, make_observation()) == keys_of(5, make_observation())
