import io
import json
from collections.abc import Callable

from nhbot.loop.step import Step
from nhbot.telemetry.event import Event
from nhbot.telemetry.json_lines_writer import JsonLinesWriter


def written_lines(make_step: Callable[..., Step], *kinds: str) -> list[str]:
    stream = io.StringIO()
    writer = JsonLinesWriter(stream, "20261013-120000-seed4")
    for kind in kinds:
        writer.write(Event.at(make_step(), kind))
    return stream.getvalue().splitlines()


def test_writes_one_line_per_event(make_step: Callable[..., Step]) -> None:
    assert len(written_lines(make_step, "message", "prompt")) == 2


def test_puts_the_game_id_first(make_step: Callable[..., Step]) -> None:
    assert next(iter(json.loads(written_lines(make_step, "message")[0]))) == "game"


def test_writes_the_kind(make_step: Callable[..., Step]) -> None:
    assert json.loads(written_lines(make_step, "message")[0])["kind"] == "message"
