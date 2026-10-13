"""Names one screen type: its kind (a prompt or a message) and its normalized text.

Output: a file name that a person can read and that is different for each key.
"""

import hashlib
import re
from dataclasses import dataclass

NOT_SLUG = re.compile(r"[^a-z0-9]+")
SLUG_LENGTH = 40


@dataclass(frozen=True)
class SampleKey:
    kind: str
    text: str

    def file_name(self) -> str:
        slug = NOT_SLUG.sub("-", self.text.lower()).strip("-")[:SLUG_LENGTH]
        digest = hashlib.sha1(f"{self.kind}:{self.text}".encode()).hexdigest()[:8]
        return f"{self.kind}--{slug}-{digest}.json"
