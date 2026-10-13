import io
import re
from collections.abc import Callable

import pytest

from nhbot.adapter.action import Action
from nhbot.adapter.key import Key
from nhbot.adapter.observation import Observation
from nhbot.loop.step import Step
from nhbot.strategy.decision import Decision
from nhbot.view.terminal_view import HIDE_CURSOR, HOME, SHOW_CURSOR, TerminalView

ANSI_CODE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


@pytest.fixture
def draw(make_observation: Callable[..., Observation]) -> Callable[..., str]:
    def drawn(decision: Decision | None = None, **changes: object) -> str:
        stream = io.StringIO()
        TerminalView(stream, "nhbot   seed 4").on_step(
            Step(3, make_observation(**changes), decision)
        )
        return stream.getvalue()

    return drawn


def plain(text: str) -> str:
    return ANSI_CODE.sub("", text)


def test_draws_from_the_home_position(draw: Callable[..., str]) -> None:
    assert draw().startswith(HOME)


def test_draws_the_screen_text(draw: Callable[..., str]) -> None:
    assert "Hello" in plain(draw(screen=("Hello".ljust(80),) + (" " * 80,) * 23))


def test_paints_red_cells_red(draw: Callable[..., str]) -> None:
    assert "\x1b[31m" in draw(colors=(bytes([1] * 80),) * 24)


def test_paints_black_as_dark_gray(draw: Callable[..., str]) -> None:
    assert "\x1b[90m" in draw()


def test_shows_the_title(draw: Callable[..., str]) -> None:
    assert "nhbot   seed 4" in plain(draw())


def test_shows_the_reason(draw: Callable[..., str]) -> None:
    assert "why     random walk" in plain(draw(Decision(Action("k"), "random walk")))


def test_names_the_enter_key(draw: Callable[..., str]) -> None:
    assert "key     Enter" in plain(draw(Decision(Action(Key.ENTER), "more")))


def test_entering_hides_the_cursor() -> None:
    stream = io.StringIO()
    with TerminalView(stream, "title"):
        assert HIDE_CURSOR in stream.getvalue()


def test_leaving_shows_the_cursor() -> None:
    stream = io.StringIO()
    with TerminalView(stream, "title"):
        pass
    assert stream.getvalue().endswith(SHOW_CURSOR + "\n")
