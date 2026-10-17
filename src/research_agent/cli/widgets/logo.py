"""The AUTOML banner shown at the top of the TUI."""

from __future__ import annotations

from textual.widgets import Static

from .. import __version__
from ..theme import logo_renderable


class LogoBanner(Static):
    """Renders the gradient wordmark, version and working directory."""

    def __init__(self, cwd: str = "", id: str | None = None) -> None:
        super().__init__(logo_renderable(__version__, cwd), id=id or "logo")
