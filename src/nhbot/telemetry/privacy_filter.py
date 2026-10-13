"""Removes the home folder path, which holds the user name, from text that goes into a bundle."""


class PrivacyFilter:
    def __init__(self, home: str) -> None:
        self._home = home.rstrip("/")

    def clean(self, text: str) -> str:
        return text.replace(self._home, "~") if self._home else text
