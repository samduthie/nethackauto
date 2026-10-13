import os
import termios
from collections.abc import Iterator

import pytest

from nhbot.view.keyboard import Keyboard


@pytest.fixture
def terminal() -> Iterator[tuple[int, int]]:
    controller, follower = os.openpty()
    yield controller, follower
    os.close(controller)
    os.close(follower)


def test_reads_one_key(terminal: tuple[int, int]) -> None:
    controller, follower = terminal
    with Keyboard(follower) as keyboard:
        os.write(controller, b"x")
        assert keyboard.read_key(1.0) == "x"


def test_gives_none_after_the_timeout(terminal: tuple[int, int]) -> None:
    with Keyboard(terminal[1]) as keyboard:
        assert keyboard.read_key(0.01) is None


def test_restores_the_terminal_settings(terminal: tuple[int, int]) -> None:
    settings_before = termios.tcgetattr(terminal[1])
    with Keyboard(terminal[1]):
        pass
    assert termios.tcgetattr(terminal[1]) == settings_before
