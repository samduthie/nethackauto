from collections.abc import Callable

import pytest
from fakes.fake_game import FakeGame
from fakes.fixed_policy import FixedPolicy
from fakes.recording_listener import RecordingListener

from nhbot.adapter.action import Action
from nhbot.adapter.observation import Observation
from nhbot.loop.game_loop import GameLoop
from nhbot.strategy.decision import Decision

DECISION = Decision(Action("s"), "test")


@pytest.fixture
def play(make_observation: Callable[..., Observation]) -> Callable[..., RecordingListener]:
    def run(game: FakeGame | None = None, max_steps: int = 3) -> RecordingListener:
        listener = RecordingListener()
        played_game = game or FakeGame([make_observation()])
        GameLoop(played_game, FixedPolicy(DECISION), [listener], max_steps).run()
        return listener

    return run


def test_tells_the_listeners_each_step_up_to_the_limit(
    play: Callable[..., RecordingListener],
) -> None:
    assert [step.number for step in play().steps] == [0, 1, 2, 3]


def test_first_step_has_no_decision(play: Callable[..., RecordingListener]) -> None:
    assert play().steps[0].decision is None


def test_later_steps_have_the_decision(play: Callable[..., RecordingListener]) -> None:
    assert play().steps[1].decision == DECISION


def test_sends_the_policy_action(
    play: Callable[..., RecordingListener], make_observation: Callable[..., Observation]
) -> None:
    game = FakeGame([make_observation()])
    play(game)
    assert game.actions == [Action("s")] * 3


def test_stops_when_the_game_is_over(
    play: Callable[..., RecordingListener], make_observation: Callable[..., Observation]
) -> None:
    game = FakeGame([make_observation(), make_observation(game_over=True)])
    assert len(play(game, max_steps=10).steps) == 2
