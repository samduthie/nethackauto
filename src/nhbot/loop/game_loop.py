"""Plays one game. Asks the policy for each action and tells the listeners about each step."""

from collections.abc import Sequence

from nhbot.adapter.game import Game
from nhbot.loop.step import Step
from nhbot.loop.step_listener import StepListener
from nhbot.strategy.policy import Policy


class GameLoop:
    def __init__(
        self, game: Game, policy: Policy, listeners: Sequence[StepListener], max_steps: int
    ) -> None:
        self._game = game
        self._policy = policy
        self._listeners = listeners
        self._max_steps = max_steps

    def run(self) -> None:
        step = Step(0, self._game.start(), None)
        while True:
            for listener in self._listeners:
                listener.on_step(step)
            if step.observation.game_over or step.number >= self._max_steps:
                return
            decision = self._policy.decide(step.observation)
            step = Step(step.number + 1, self._game.send(decision.action), decision)
