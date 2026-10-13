"""A KeySource that gives a list of keys. With no keys left, it waits for the timeout."""

from fakes.fake_clock import FakeClock


class FakeKeyboard:
    def __init__(self, keys: str, clock: FakeClock) -> None:
        self.keys = list(keys)
        self.clock = clock

    def read_key(self, timeout: float | None) -> str | None:
        if self.keys:
            return self.keys.pop(0)
        self.clock.now += timeout or 0.0
        return None
