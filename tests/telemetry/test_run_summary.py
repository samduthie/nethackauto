from collections.abc import Callable

from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.observation import Observation
from nhbot.loop.step import Step
from nhbot.telemetry.run_summary import RunSummary


def summary_line(observations: list[Observation]) -> str:
    summary = RunSummary(seed=4)
    for number, observation in enumerate(observations):
        summary.on_step(Step(number, observation, None))
    return summary.line()


def test_reports_the_seed_and_step_count(make_observation: Callable[..., Observation]) -> None:
    assert summary_line([make_observation()] * 8).startswith("seed 4: stopped after 7 steps")


def test_reports_game_over(make_observation: Callable[..., Observation]) -> None:
    assert "game over" in summary_line([make_observation(game_over=True)])


def test_keeps_the_max_depth_after_the_end_screens(
    make_observation: Callable[..., Observation], make_bottom_line: Callable[..., BottomLine]
) -> None:
    depths = [2, 3, 0]  # NLE sets the stats to 0 on the end screens
    observations = [make_observation(bottom_line=make_bottom_line(depth=d)) for d in depths]
    assert summary_line(observations).endswith("max depth 3")


def test_keeps_the_last_turn_after_the_end_screens(
    make_observation: Callable[..., Observation], make_bottom_line: Callable[..., BottomLine]
) -> None:
    turns = [5, 9, 0]
    observations = [make_observation(bottom_line=make_bottom_line(turn=t)) for t in turns]
    assert "turn 9," in summary_line(observations)
