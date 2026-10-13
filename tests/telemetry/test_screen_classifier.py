from collections.abc import Callable

from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.observation import Observation
from nhbot.telemetry.sample_key import SampleKey
from nhbot.telemetry.screen_classifier import ScreenClassifier

EAT_QUESTION = "What do you want to eat? [d or ?*]"  # seen in play after the key e


def top_line(text: str) -> tuple[str, ...]:
    return (text.ljust(80),) + (" " * 80,) * 23


def test_names_a_prompt_by_its_question(make_observation: Callable[..., Observation]) -> None:
    observation = make_observation(
        screen=top_line(EAT_QUESTION), message=EAT_QUESTION + " ", input_mode=InputMode.KEY_PROMPT
    )
    assert ScreenClassifier().keys(observation) == [
        SampleKey("key_prompt", "What do you want to eat? [...]")
    ]


def test_gives_one_key_for_each_sentence(make_observation: Callable[..., Observation]) -> None:
    observation = make_observation(message="The fox just misses!  The fox bites!")
    assert [key.text for key in ScreenClassifier().keys(observation)] == [
        "The fox just misses!",
        "The fox bites!",
    ]


def test_replaces_numbers(make_observation: Callable[..., Observation]) -> None:
    observation = make_observation(message="12 gold pieces.")
    assert ScreenClassifier().keys(observation) == [SampleKey("message", "# gold pieces.")]


def test_gives_nothing_without_a_message(make_observation: Callable[..., Observation]) -> None:
    assert ScreenClassifier().keys(make_observation()) == []


def test_keeps_quoted_text_in_one_sentence(make_observation: Callable[..., Observation]) -> None:
    message = 'Something is written here in the dust.  You read: "a  ?cr   u?".'  # seen in play
    assert [key.text for key in ScreenClassifier().keys(make_observation(message=message))] == [
        "Something is written here in the dust.",
        'You read: "...".',
    ]
