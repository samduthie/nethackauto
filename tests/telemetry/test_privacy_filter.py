from nhbot.telemetry.privacy_filter import PrivacyFilter


def test_replaces_the_home_folder() -> None:
    assert (
        PrivacyFilter("/home/alice").clean('File "/home/alice/nhbot/main.py"')
        == 'File "~/nhbot/main.py"'
    )


def test_keeps_other_text() -> None:
    assert PrivacyFilter("/home/alice").clean("The fox bites!") == "The fox bites!"


def test_keeps_text_when_home_is_the_root() -> None:
    assert PrivacyFilter("/").clean("/usr/lib") == "/usr/lib"
