"""One game frame in our own types. The adapter makes it. All other packages read it."""

from dataclasses import dataclass

from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.input_mode import InputMode


@dataclass(frozen=True)
class Observation:
    screen: tuple[str, ...]  # 24 rows of 80 characters, as on the terminal
    colors: tuple[bytes, ...]  # 24 rows of 80 color numbers (0 to 15)
    cursor: tuple[int, int]  # (row, column)
    glyphs: tuple[tuple[int, ...], ...]  # 21 map rows of 79 glyph numbers
    message: str
    bottom_line: BottomLine
    input_mode: InputMode
    game_over: bool
