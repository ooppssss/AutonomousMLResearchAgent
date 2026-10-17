"""Scrollable conversation view for the automl TUI."""

from __future__ import annotations

from textual.widgets import RichLog

from ..theme import (
    agent_panel,
    error_panel,
    system_panel,
    tool_panel,
    user_panel,
)


class Conversation(RichLog):
    """A read-only, auto-scrolling log of the session."""

    def __init__(self, id: str | None = None) -> None:
        super().__init__(
            highlight=False,
            markup=False,
            wrap=True,
            id=id or "conversation",
        )

    def add_user(self, message: str) -> None:
        self.write(user_panel(message))

    def add_agent(self, message: str) -> None:
        self.write(agent_panel(message))

    def add_system(self, message: str) -> None:
        self.write(system_panel(message))

    def add_error(self, message: str) -> None:
        self.write(error_panel(message))

    def add_tool(self, title: str, message: str, *, ok: bool = True) -> None:
        self.write(tool_panel(title, message, ok=ok))
