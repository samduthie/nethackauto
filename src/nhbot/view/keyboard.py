"""Reads one key at a time from a terminal, with no Enter. Linux and macOS only."""

import os
import select
import termios
import tty
from typing import Any, Self


class Keyboard:
    def __init__(self, file_descriptor: int) -> None:
        self._file_descriptor = file_descriptor
        self._saved_settings: list[Any] = []

    def __enter__(self) -> Self:
        self._saved_settings = termios.tcgetattr(self._file_descriptor)
        tty.setcbreak(self._file_descriptor)  # ctrl-c still works
        return self

    def __exit__(self, *exception_info: object) -> None:
        termios.tcsetattr(self._file_descriptor, termios.TCSADRAIN, self._saved_settings)

    def read_key(self, timeout: float | None) -> str | None:
        ready, _, _ = select.select([self._file_descriptor], [], [], timeout)
        return os.read(self._file_descriptor, 1).decode("latin-1") if ready else None
