"""Prompt input with slash-command autocomplete."""

from __future__ import annotations

from collections.abc import Iterable

from textual.suggester import SuggestFromList
from textual.widgets import Input

PLACEHOLDER = "Ask anything   ·   / for commands   ·   ! for shell"


class PromptInput(Input):
    """Input box that suggests registered slash commands as you type."""

    def __init__(self, suggestions: Iterable[str], id: str | None = None) -> None:
        super().__init__(
            placeholder=PLACEHOLDER,
            suggester=SuggestFromList(list(suggestions), case_sensitive=False),
            id=id or "prompt",
        )

    def set_suggestions(self, suggestions: Iterable[str]) -> None:
        self.suggester = SuggestFromList(
            list(suggestions),
            case_sensitive=False,
        )
