"""Draws each step in the terminal: the game screen in color and a side panel.

It only reads the step. It never changes a decision.
"""

from itertools import groupby, zip_longest
from operator import itemgetter
from typing import Self, TextIO

from nhbot.loop.step import Step

# NetHack color number -> ANSI color code. Black (0) shows as dark gray.
DEFAULT_COLOR = 37
DARK_COLORS = {color: 30 + color for color in range(1, 8)}
BRIGHT_COLORS = {color: 82 + color for color in range(9, 16)}
ANSI_COLORS = {0: 90, 8: DEFAULT_COLOR} | DARK_COLORS | BRIGHT_COLORS
HOME, CLEAR_SCREEN, CLEAR_LINE_END = "\x1b[H", "\x1b[2J", "\x1b[K"
HIDE_CURSOR, SHOW_CURSOR, RESET = "\x1b[?25l", "\x1b[?25h", "\x1b[0m"
KEY_NAMES = {"\r": "Enter", "\x1b": "Esc"}
HELP_LINES = (
    "",
    "space   pause / resume",
    ".       one step",
    "+ / -   faster / slower",
    "ctrl-c  quit",
)


class TerminalView:
    def __init__(self, stream: TextIO, title: str) -> None:
        self._stream = stream
        self._title = title

    def __enter__(self) -> Self:
        self._stream.write(CLEAR_SCREEN + HIDE_CURSOR)
        return self

    def __exit__(self, *exception_info: object) -> None:
        self._stream.write(RESET + SHOW_CURSOR + "\n")
        self._stream.flush()

    def on_step(self, step: Step) -> None:
        observation = step.observation
        rows = zip(observation.screen, observation.colors, strict=True)
        lines = zip_longest(rows, self._panel(step), fillvalue=None)
        self._stream.write(HOME + "\n".join(self._line(row, text) for row, text in lines))
        self._stream.flush()

    def _line(self, row: tuple[str, bytes] | None, panel_text: str | None) -> str:
        painted = self._paint(*row) if row else ""
        return f"{painted}  {panel_text or ''}{CLEAR_LINE_END}"

    def _panel(self, step: Step) -> list[str]:
        decision = step.decision
        key = KEY_NAMES.get(decision.action.key, decision.action.key) if decision else "-"
        reason = decision.reason if decision else "start"
        status = [f"step    {step.number}", f"key     {key}", f"why     {reason}"]
        return [self._title, *status, *HELP_LINES]

    @staticmethod
    def _paint(text: str, colors: bytes) -> str:
        painted = ""
        for color, cells in groupby(zip(text, colors, strict=True), key=itemgetter(1)):
            painted += f"\x1b[{ANSI_COLORS.get(color, DEFAULT_COLOR)}m" + "".join(
                c for c, _ in cells
            )
        return painted + RESET
