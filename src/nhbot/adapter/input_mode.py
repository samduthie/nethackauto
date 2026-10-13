"""What kind of input the game waits for."""

from enum import Enum, auto


class InputMode(Enum):
    COMMAND = auto()
    MORE = auto()  # "--More--": only Enter, space or Escape continue
    KEY_PROMPT = auto()  # a question that takes one key, for example "[ynq]"
    TEXT_PROMPT = auto()  # a question that takes a line of text, for example an engraving
