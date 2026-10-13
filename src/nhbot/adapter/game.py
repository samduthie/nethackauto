"""The game as the bot sees it. Input: Actions. Output: Observations."""

from typing import Protocol

from nhbot.adapter.action import Action
from nhbot.adapter.observation import Observation


class Game(Protocol):
    def start(self) -> Observation: ...

    def send(self, action: Action) -> Observation: ...
