from pathlib import Path

from nhbot.telemetry.code_version import CodeVersion


def test_reads_the_git_version_in_the_repository() -> None:
    assert CodeVersion(Path(__file__).parent).read() != "unknown"


def test_gives_unknown_outside_a_repository(tmp_path: Path) -> None:
    assert CodeVersion(tmp_path).read() == "unknown"
