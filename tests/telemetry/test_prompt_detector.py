from collections.abc import Callable

import pytest

from nhbot.adapter.input_mode import InputMode
from nhbot.loop.step import Step
from nhbot.telemetry.prompt_detector import PromptDetector

QUESTION = "What do you want to write with? [- ab or ?*]"  # seen in play after the key E


@pytest.fixture
def question_step(make_step: Callable[..., Step]) -> Step:
    screen = (QUESTION.ljust(80),) + (" " * 80,) * 23
    return make_step(screen=screen, input_mode=InputMode.KEY_PROMPT)


def test_gives_a_prompt_event(question_step: Step) -> None:
    assert [event.kind for event in PromptDetector().detect(None, question_step)] == ["prompt"]


def test_keeps_the_question(question_step: Step) -> None:
    assert PromptDetector().detect(None, question_step)[0].fields["text"] == QUESTION


def test_keeps_the_mode(question_step: Step) -> None:
    assert PromptDetector().detect(None, question_step)[0].fields["mode"] == "key_prompt"


def test_gives_the_same_question_once(question_step: Step) -> None:
    assert PromptDetector().detect(question_step, question_step) == []


@pytest.mark.parametrize("input_mode", [InputMode.COMMAND, InputMode.MORE])
def test_ignores_other_modes(make_step: Callable[..., Step], input_mode: InputMode) -> None:
    assert PromptDetector().detect(None, make_step(input_mode=input_mode)) == []
