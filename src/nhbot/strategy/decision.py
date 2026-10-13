"""An action and the reason for it. The reason goes to the view and to the logs."""

from dataclasses import dataclass

from nhbot.adapter.action import Action


@dataclass(frozen=True)
class Decision:
    action: Action
    reason: str
