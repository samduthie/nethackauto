"""Plays one game. This is the composition root: it makes all objects and connects them.

Each run writes its files to runs/<game id>/: events.jsonl and one bundle for each incident.
"""

import random
import sys
import time
from collections.abc import Sequence
from contextlib import ExitStack, suppress
from datetime import datetime
from pathlib import Path

from nhbot.adapter.nle_game import NleGame
from nhbot.adapter.observation_reader import ObservationReader
from nhbot.loop.game_loop import GameLoop
from nhbot.loop.step_listener import StepListener
from nhbot.run_options import RunOptions
from nhbot.strategy.random_walk import RandomWalk
from nhbot.telemetry.bundle_format import BundleFormat
from nhbot.telemetry.code_version import CodeVersion
from nhbot.telemetry.event_detector import EventDetector
from nhbot.telemetry.event_log import EventLog
from nhbot.telemetry.event_sink import EventSink
from nhbot.telemetry.flight_recorder import FlightRecorder
from nhbot.telemetry.game_over_detector import GameOverDetector
from nhbot.telemetry.game_over_trigger import GameOverTrigger
from nhbot.telemetry.game_start_detector import GameStartDetector
from nhbot.telemetry.incident_trigger import IncidentTrigger
from nhbot.telemetry.json_lines_writer import JsonLinesWriter
from nhbot.telemetry.message_detector import MessageDetector
from nhbot.telemetry.privacy_filter import PrivacyFilter
from nhbot.telemetry.prompt_detector import PromptDetector
from nhbot.telemetry.recent_events import RecentEvents
from nhbot.telemetry.run_info import RunInfo
from nhbot.telemetry.run_summary import RunSummary
from nhbot.telemetry.stall_trigger import StallTrigger
from nhbot.telemetry.status_change_detector import StatusChangeDetector
from nhbot.view.keyboard import Keyboard
from nhbot.view.playback_control import PlaybackControl
from nhbot.view.terminal_view import TerminalView

LOGGED_STATUS_FIELDS = (
    "depth",
    "dungeon_number",
    "hit_points",
    "max_hit_points",
    "experience_level",
    "hunger_state",
    "conditions",
    "armor_class",
    "gold",
    "carrying_capacity",
)
RECENT_EVENTS_KEPT = 500  # source: brief section 7.2


def main(arguments: Sequence[str] | None = None) -> None:
    options = RunOptions.parse(arguments)
    game_id = f"{datetime.now():%Y%m%d-%H%M%S}-seed{options.seed}"
    code_version = CodeVersion(Path(__file__).parent).read()
    run_info = RunInfo(game_id, options.seed, options.character, code_version)
    run_directory = options.runs_directory / game_id
    run_directory.mkdir(parents=True, exist_ok=True)
    summary = RunSummary(options.seed)
    policy = RandomWalk(random.Random(options.seed))
    game = NleGame(options.seed, options.character, ObservationReader())
    try:
        with suppress(KeyboardInterrupt), game, ExitStack() as stack:
            listeners = [summary, *telemetry(stack, run_info, run_directory)]
            if options.watch:
                listeners += watch_view(stack, options)
            GameLoop(game, policy, listeners, options.max_steps).run()
    finally:
        print(f"run files: {run_directory}")
    print(summary.line())


def telemetry(stack: ExitStack, run_info: RunInfo, run_directory: Path) -> list[StepListener]:
    # Exit order is the reverse of entry: the event log writes run_end, then the recorder
    # saves an exception bundle, then the events file closes.
    events_file = (run_directory / "events.jsonl").open("w", encoding="utf-8", buffering=1)
    stack.enter_context(events_file)
    recent_events = RecentEvents(RECENT_EVENTS_KEPT)
    bundle_format = BundleFormat(run_info, PrivacyFilter(str(Path.home())))
    triggers: list[IncidentTrigger] = [GameOverTrigger(), StallTrigger()]
    recorder = FlightRecorder(run_directory, bundle_format, recent_events, triggers)
    stack.enter_context(recorder)
    sinks: list[EventSink] = [JsonLinesWriter(events_file, run_info.game_id), recent_events]
    event_log = stack.enter_context(EventLog(event_detectors(run_info), sinks))
    return [event_log, recorder]


def event_detectors(run_info: RunInfo) -> list[EventDetector]:
    status_changes = [StatusChangeDetector(field) for field in LOGGED_STATUS_FIELDS]
    return [
        GameStartDetector(run_info),
        *status_changes,
        MessageDetector(),
        PromptDetector(),
        GameOverDetector(),
    ]


def watch_view(stack: ExitStack, options: RunOptions) -> list[StepListener]:
    keyboard = stack.enter_context(Keyboard(sys.stdin.fileno()))
    view = stack.enter_context(TerminalView(sys.stdout, f"nhbot   seed {options.seed}"))
    return [view, PlaybackControl(keyboard, options.delay, time.monotonic)]


if __name__ == "__main__":
    main()
