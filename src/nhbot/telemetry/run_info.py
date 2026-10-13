"""Facts about one run for the event log and each bundle. No paths and no user names."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RunInfo:
    game_id: str
    seed: int
    character: str
    code_version: str
