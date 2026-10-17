"""One-line status bar pinned to the bottom of the TUI."""

from __future__ import annotations

from rich.text import Text
from textual.widgets import Static

from ..theme import ACCENT, MUTED, SUCCESS


class StatusBar(Static):
    """Shows the active model, working directory and key hints."""

    def __init__(self, cwd: str = "", model: str = "no-model", id: str | None = None) -> None:
        super().__init__(id=id or "status")
        self._cwd = cwd
        self._model = model
        self._state = "ready"
        self._refresh()

    def _refresh(self) -> None:
        text = Text(no_wrap=True, overflow="ellipsis")
        text.append("● ", style=SUCCESS)
        text.append(self._state, style=SUCCESS)
        text.append("  ")
        text.append(self._model, style=ACCENT)
        text.append("  ")
        text.append(self._cwd, style=MUTED)
        text.append("   ")
        text.append("ctrl+q quit  ·  ctrl+l clear  ·  f1 help", style=MUTED)
        self.update(text)

    def set_model(self, model: str) -> None:
        self._model = model
        self._refresh()

    def set_state(self, state: str) -> None:
        self._state = state
        self._refresh()
