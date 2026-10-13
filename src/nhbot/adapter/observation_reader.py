"""Turns one NLE observation (a dict of arrays) into our Observation."""

from collections.abc import Mapping
from typing import Any

from numpy.typing import NDArray

from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.observation import Observation


class ObservationReader:
    def read(self, nle_observation: Mapping[str, NDArray[Any]], game_over: bool) -> Observation:
        cursor_row, cursor_column = nle_observation["tty_cursor"].tolist()
        return Observation(
            screen=tuple(self._text(line) for line in nle_observation["tty_chars"]),
            colors=tuple(line.tobytes() for line in nle_observation["tty_colors"]),
            cursor=(cursor_row, cursor_column),
            glyphs=tuple(map(tuple, nle_observation["glyphs"].tolist())),
            message=self._text(nle_observation["message"]).rstrip("\0"),
            bottom_line=BottomLine(*nle_observation["blstats"].tolist()),
            input_mode=self._input_mode(nle_observation["misc"].tolist()),
            game_over=game_over,
        )

    @staticmethod
    def _text(codes: NDArray[Any]) -> str:
        return codes.tobytes().decode("latin-1")

    @staticmethod
    def _input_mode(misc: list[int]) -> InputMode:
        # "--More--" comes first: the game can show it while a text prompt waits.
        in_key_prompt, in_text_prompt, in_more = misc
        if in_more:
            return InputMode.MORE
        if in_key_prompt:
            return InputMode.KEY_PROMPT
        if in_text_prompt:
            return InputMode.TEXT_PROMPT
        return InputMode.COMMAND
