from collections.abc import Callable, Iterator

import pytest

from nhbot.adapter.action import Action
from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.key import Key
from nhbot.adapter.nle_game import NleGame
from nhbot.adapter.observation import Observation
from nhbot.adapter.observation_reader import ObservationReader

CHARACTER = "val-dwa-law-fem"
StartScreen = Callable[[int], tuple[str, ...]]


@pytest.fixture
def game() -> Iterator[NleGame]:
    with NleGame(1, CHARACTER, ObservationReader()) as started_game:
        yield started_game


@pytest.fixture
def start_screen() -> StartScreen:
    def start(seed: int) -> tuple[str, ...]:
        with NleGame(seed, CHARACTER, ObservationReader()) as new_game:
            return new_game.start().screen

    return start


def send_keys(game: NleGame, keys: str) -> Observation:
    observation = game.start()
    for key in keys:
        observation = game.send(Action(key))
    return observation


def test_same_seed_gives_the_same_start_screen(start_screen: StartScreen) -> None:
    assert start_screen(1) == start_screen(1)


def test_other_seed_gives_another_start_screen(start_screen: StartScreen) -> None:
    assert start_screen(1) != start_screen(2)


def test_starts_a_dwarvish_valkyrie(start_screen: StartScreen) -> None:
    assert "dwarven Valkyrie" in start_screen(1)[0]


def test_search_uses_one_turn(game: NleGame) -> None:
    assert send_keys(game, "s").bottom_line.turn == 2


def test_engrave_asks_for_a_key(game: NleGame) -> None:
    assert send_keys(game, "E").input_mode is InputMode.KEY_PROMPT


def test_engrave_in_the_dust_asks_for_text(game: NleGame) -> None:
    assert send_keys(game, "E-" + Key.ENTER).input_mode is InputMode.TEXT_PROMPT


def test_unknown_key_raises(game: NleGame) -> None:
    with pytest.raises(ValueError, match="no action"):
        send_keys(game, "~")
