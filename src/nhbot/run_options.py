"""The command-line options for one game."""

import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass(frozen=True)
class RunOptions:
    seed: int
    max_steps: int
    watch: bool
    delay: float
    character: str
    runs_directory: Path
    samples_directory: Path

    @classmethod
    def parse(cls, arguments: Sequence[str] | None) -> Self:
        parser = argparse.ArgumentParser(prog="nhbot", description="Play one NetHack game.")
        parser.add_argument("--seed", type=int, default=1)
        parser.add_argument("--steps", type=int, default=1000, dest="max_steps")
        parser.add_argument("--watch", action="store_true", help="draw the game in the terminal")
        parser.add_argument("--delay", type=float, default=0.1, help="seconds per watched step")
        parser.add_argument("--character", default="val-dwa-law-fem")
        parser.add_argument("--runs-dir", type=Path, default=Path("runs"), dest="runs_directory")
        parser.add_argument(
            "--samples-dir", type=Path, default=Path("samples"), dest="samples_directory"
        )
        return cls(**vars(parser.parse_args(arguments)))
