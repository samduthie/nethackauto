from nhbot.telemetry.sample_key import SampleKey


def test_names_the_file_with_the_kind_and_the_text() -> None:
    name = SampleKey("key_prompt", "What do you want to eat? [...]").file_name()
    assert name.startswith("key_prompt--what-do-you-want-to-eat-")


def test_gives_the_same_name_for_the_same_key() -> None:
    assert (
        SampleKey("message", "It's a wall.").file_name()
        == SampleKey("message", "It's a wall.").file_name()
    )


def test_gives_another_name_for_another_text() -> None:
    assert (
        SampleKey("message", "It's a wall.").file_name()
        != SampleKey("message", "It's a wall!").file_name()
    )


def test_ends_the_name_with_json() -> None:
    assert SampleKey("message", "The fox bites!").file_name().endswith(".json")
