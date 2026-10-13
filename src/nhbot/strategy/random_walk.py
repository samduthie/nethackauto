"""Walks and searches at random. A placeholder until exploration (task T6) and prompts (task T7)."""

import random

from nhbot.adapter.action import Action
from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.key import Key
from nhbot.adapter.observation import Observation
from nhbot.strategy.decision import Decision

SAFE_KEYS = "hjklyubns"  # the eight moves and search


class RandomWalk:
    def __init__(self, randomizer: random.Random) -> None:
        self._randomizer = randomizer

    def decide(self, observation: Observation) -> Decision:
        if observation.input_mode is InputMode.MORE:
            return Decision(Action(Key.ENTER), "continue after --More--")
        if observation.input_mode is not InputMode.COMMAND:
            return Decision(Action(Key.ESCAPE), "decline the prompt")
        return Decision(Action(self._randomizer.choice(SAFE_KEYS)), "random walk")
