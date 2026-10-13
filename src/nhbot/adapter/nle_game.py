"""Runs one seeded NetHack game in NLE. Input: Actions. Output: Observations.

This is the only class that starts NLE.
"""

from dataclasses import replace
from typing import Self

from nle import nethack
from nle.env.base import NLE

from nhbot.adapter.action import Action
from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.observation import Observation
from nhbot.adapter.observation_reader import ObservationReader

OBSERVATION_KEYS = ("glyphs", "blstats", "message", "misc", "tty_chars", "tty_colors", "tty_cursor")
NO_STEP_LIMIT = 10**9  # the game loop sets the real limit


class NleGame:
    def __init__(self, seed: int, character: str, reader: ObservationReader) -> None:
        self._seed = seed
        self._reader = reader
        self._last_bottom_line: BottomLine | None = None
        self._action_index = {
            chr(int(action)): index for index, action in enumerate(nethack.ACTIONS)
        }
        self._env = NLE(
            character=character,
            actions=nethack.ACTIONS,
            observation_keys=OBSERVATION_KEYS,
            max_episode_steps=NO_STEP_LIMIT,
            allow_all_yn_questions=True,  # the bot answers all prompts itself
            allow_all_modes=True,
            fix_moon_phase=True,  # moon phase and dates come from the seed, not from the clock
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exception_info: object) -> None:
        self._env.close()

    def start(self) -> Observation:
        self._env.seed(self._seed, self._seed, False)
        nle_observation, _ = self._env.reset()
        return self._keep_status(self._reader.read(nle_observation, game_over=False))

    def send(self, action: Action) -> Observation:
        nle_observation, _, terminated, truncated, _ = self._env.step(self._index_of(action))
        return self._keep_status(
            self._reader.read(nle_observation, game_over=terminated or truncated)
        )

    def _keep_status(self, observation: Observation) -> Observation:
        # NLE sets all status values to 0 on the game-over frame. Keep the last real values.
        if observation.bottom_line.depth == 0 and self._last_bottom_line:
            return replace(observation, bottom_line=self._last_bottom_line)
        self._last_bottom_line = observation.bottom_line
        return observation

    def _index_of(self, action: Action) -> int:
        if action.key not in self._action_index:
            raise ValueError(f"NLE has no action for the key {action.key!r}")
        return self._action_index[action.key]
