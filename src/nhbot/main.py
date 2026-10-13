"""Plays one game. This is the composition root: it makes all objects and connects them."""

import random
import sys
import time
from collections.abc import Sequence
from contextlib import ExitStack, suppress

from nhbot.adapter.nle_game import NleGame
from nhbot.adapter.observation_reader import ObservationReader
from nhbot.loop.game_loop import GameLoop
from nhbot.loop.step_listener import StepListener
from nhbot.run_options import RunOptions
from nhbot.strategy.random_walk import RandomWalk
from nhbot.telemetry.run_summary import RunSummary
from nhbot.view.keyboard import Keyboard
from nhbot.view.playback_control import PlaybackControl
from nhbot.view.terminal_view import TerminalView


def main(arguments: Sequence[str] | None = None) -> None:
    options = RunOptions.parse(arguments)
    summary = RunSummary(options.seed)
    listeners: list[StepListener] = [summary]
    policy = RandomWalk(random.Random(options.seed))
    game = NleGame(options.seed, options.character, ObservationReader())
    with game, ExitStack() as stack:
        if options.watch:
            keyboard = stack.enter_context(Keyboard(sys.stdin.fileno()))
            view = TerminalView(sys.stdout, f"nhbot   seed {options.seed}")
            listeners.append(stack.enter_context(view))
            listeners.append(PlaybackControl(keyboard, options.delay, time.monotonic))
        with suppress(KeyboardInterrupt):
            GameLoop(game, policy, listeners, options.max_steps).run()
    print(summary.line())


if __name__ == "__main__":
    main()
