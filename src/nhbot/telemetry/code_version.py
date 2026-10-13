"""Reads the git version of the code, for example "49d00ab-dirty", or "unknown" without git."""

import subprocess
from pathlib import Path

GIT_DESCRIBE = ["git", "describe", "--always", "--dirty"]


class CodeVersion:
    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def read(self) -> str:
        try:
            result = subprocess.run(
                GIT_DESCRIBE,
                cwd=self._directory,
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            )
        except (OSError, subprocess.SubprocessError):
            return "unknown"
        return result.stdout.strip() or "unknown"
