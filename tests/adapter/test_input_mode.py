import pytest

from nhbot.adapter.input_mode import InputMode


@pytest.mark.parametrize(
    ("input_mode", "is_prompt"),
    [
        (InputMode.KEY_PROMPT, True),
        (InputMode.TEXT_PROMPT, True),
        (InputMode.COMMAND, False),
        (InputMode.MORE, False),
    ],
)
def test_knows_which_modes_are_prompts(input_mode: InputMode, is_prompt: bool) -> None:
    assert input_mode.is_prompt is is_prompt
