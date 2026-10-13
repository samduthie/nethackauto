"""Keeps one sample file for each screen type in a folder. Input: key and content. Output: files."""

import json
from pathlib import Path

from nhbot.telemetry.sample_key import SampleKey


class SampleStore:
    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def has(self, key: SampleKey) -> bool:
        return (self._directory / key.file_name()).exists()

    def save(self, key: SampleKey, content: dict[str, object]) -> Path:
        self._directory.mkdir(parents=True, exist_ok=True)
        path = self._directory / key.file_name()
        path.write_text(json.dumps(content, indent=1), encoding="utf-8")
        return path
