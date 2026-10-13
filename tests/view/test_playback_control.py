from collections.abc import Callable

import pytest
from fakes.fake_clock import FakeClock
from fakes.fake_keyboard import FakeKeyboard

from nhbot.adapter.observation import Observation
from nhbot.loop.step import Step
from nhbot.view.playback_control import PlaybackControl

DELAY = 0.1
Played = tuple[PlaybackControl, FakeKeyboard, FakeClock]


@pytest.fixture
def play(make_observation: Callable[..., Observation]) -> Callable[[str], Played]:
    def played(keys: str) -> Played:
        clock = FakeClock()
        keyboard = FakeKeyboard(keys, clock)
        control = PlaybackControl(keyboard, DELAY, clock)
        control.on_step(Step(0, make_observation(), None))
        return control, keyboard, clock

    return played


def test_waits_the_delay_with_no_keys(play: Callable[[str], Played]) -> None:
    assert play("")[2].now == pytest.approx(DELAY)


def test_space_pauses(play: Callable[[str], Played]) -> None:
    assert play(" .")[0].paused


def test_space_two_times_resumes(play: Callable[[str], Played]) -> None:
    assert not play("  ")[0].paused


def test_dot_plays_one_step_when_paused(play: Callable[[str], Played]) -> None:
    assert play(" .x")[1].keys == ["x"]


def test_plus_halves_the_delay(play: Callable[[str], Played]) -> None:
    assert play("+")[0].delay == pytest.approx(DELAY / 2)


def test_minus_doubles_the_delay(play: Callable[[str], Played]) -> None:
    assert play("-")[0].delay == pytest.approx(DELAY * 2)
