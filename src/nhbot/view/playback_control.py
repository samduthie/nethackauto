"""Paces watch mode. Space pauses or resumes, "." plays one step, "+" and "-" change the speed."""

from collections.abc import Callable

from nhbot.loop.step import Step
from nhbot.view.key_source import KeySource

PAUSE_KEY, STEP_KEY, FASTER_KEY, SLOWER_KEY = " ", ".", "+", "-"


class PlaybackControl:
    def __init__(self, keyboard: KeySource, delay: float, clock: Callable[[], float]) -> None:
        self._keyboard = keyboard
        self._delay = delay
        self._clock = clock
        self._paused = False

    @property
    def paused(self) -> bool:
        return self._paused

    @property
    def delay(self) -> float:
        return self._delay

    def on_step(self, step: Step) -> None:
        deadline = self._clock() + self._delay
        while self._paused or self._clock() < deadline:
            timeout = None if self._paused else max(0.0, deadline - self._clock())
            key = self._keyboard.read_key(timeout)
            if key == STEP_KEY and self._paused:
                return
            self._press(key)

    def _press(self, key: str | None) -> None:
        if key == PAUSE_KEY:
            self._paused = not self._paused
        elif key == FASTER_KEY:
            self._delay /= 2
        elif key == SLOWER_KEY:
            self._delay *= 2
