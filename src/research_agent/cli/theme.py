"""Central theme for the automl CLI.

Holds the colour palette, the ASCII wordmark, the Textual stylesheet and
small helpers that build Rich renderables for the conversation view.
Everything here is self-contained so the CLI has no dependency on the rest
of the project.
"""

from __future__ import annotations

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# ---------------------------------------------------------------------------
# Palette (Catppuccin Mocha inspired — soft, dark, modern)
# ---------------------------------------------------------------------------
BACKGROUND = "#1e1e2e"
SURFACE = "#313244"
SURFACE_DARK = "#181825"
BORDER = "#45475a"
TEXT = "#cdd6f4"
SUBTLE = "#a6adc8"
MUTED = "#6c7086"
ACCENT = "#cba6f7"
ACCENT_2 = "#89b4fa"
SUCCESS = "#a6e3a1"
WARNING = "#f9e2af"
ERROR = "#f38ba8"
OVERLAY = "#6c7086"

GRADIENT = [ACCENT, "#b4befe", ACCENT_2, "#74c7ec", "#89dceb"]

# ---------------------------------------------------------------------------
# Wordmark
# ---------------------------------------------------------------------------
WORDMARK = "AUTOML"
_LETTER_HEIGHT = 5
_LETTERS: dict[str, list[str]] = {
    "A": [" █████ ", "██   ██", "███████", "██   ██", "██   ██"],
    "U": ["██   ██", "██   ██", "██   ██", "██   ██", " █████ "],
    "T": ["███████", "   █   ", "   █   ", "   █   ", "   █   "],
    "O": [" █████ ", "██   ██", "██   ██", "██   ██", " █████ "],
    "M": ["██   ██", "███ ███", "███ ███", "██ █ ██", "██   ██"],
    "L": ["██     ", "██     ", "██     ", "██     ", "███████"],
}

WORDMARK_LINES: list[str] = [
    " ".join(_LETTERS[char][row] for char in WORDMARK)
    for row in range(_LETTER_HEIGHT)
]


# ---------------------------------------------------------------------------
# Renderable builders
# ---------------------------------------------------------------------------
def logo_renderable(version: str, cwd: str) -> Text:
    """The banner shown at the top of the TUI."""
    text = Text()
    for index, line in enumerate(WORDMARK_LINES):
        colour = GRADIENT[index % len(GRADIENT)]
        text.append(line + "\n", style=f"bold {colour}")
    text.append("autonomous ML research agent", style=f"italic {TEXT}")
    text.append(f"   v{version}\n", style=MUTED)
    text.append(cwd, style=MUTED)
    return text


def _panel(body, *, title: str, border: str, title_style: str | None = None) -> Panel:
    if isinstance(body, str):
        body = Text(body)
    return Panel(
        body,
        title=title,
        title_align="left",
        border_style=border,
        box=box.ROUNDED,
        padding=(0, 1),
    )


def user_panel(message: str) -> Panel:
    return _panel(message, title="you", border=ACCENT_2, title_style=f"bold {ACCENT_2}")


def agent_panel(message: str) -> Panel:
    return _panel(message, title="automl", border=ACCENT, title_style=f"bold {ACCENT}")


def system_panel(message: str) -> Panel:
    return _panel(message, title="system", border=BORDER, title_style=MUTED)


def error_panel(message: str) -> Panel:
    return _panel(message, title="error", border=ERROR, title_style=f"bold {ERROR}")


def tool_panel(title: str, message: str, *, ok: bool = True) -> Panel:
    border = SUCCESS if ok else ERROR
    return _panel(message, title=title, border=border, title_style=f"bold {border}")


def help_panel(commands) -> Panel:
    table = Table(
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style=f"bold {ACCENT}",
        border_style=BORDER,
        padding=(0, 2),
        expand=False,
    )
    table.add_column("command", style=ACCENT_2, no_wrap=True)
    table.add_column("aliases", style=MUTED, no_wrap=True)
    table.add_column("description", style=TEXT)
    for command in commands:
        aliases = ", ".join(f"/{alias}" for alias in command.aliases) or "—"
        table.add_row(command.usage, aliases, command.description)
    return _panel(table, title="commands", border=ACCENT, title_style=f"bold {ACCENT}")


# ---------------------------------------------------------------------------
# Textual stylesheet
# ---------------------------------------------------------------------------
APP_CSS = f"""
Screen {{
    background: {BACKGROUND};
    color: {TEXT};
}}

#logo {{
    height: auto;
    padding: 1 3 0 3;
    background: {BACKGROUND};
}}

#conversation {{
    height: 1fr;
    margin: 1 2 0 2;
    padding: 0 1;
    background: {SURFACE_DARK};
    border: round {BORDER};
    scrollbar-background: {SURFACE_DARK};
    scrollbar-color: {OVERLAY};
}}

#prompt {{
    margin: 0 2;
    border: round {ACCENT};
    background: {SURFACE};
    color: {TEXT};
}}

#prompt:focus {{
    border: round {ACCENT_2};
}}

#status {{
    height: 1;
    margin: 0 2 0 2;
    padding: 0 1;
    background: {SURFACE};
    color: {SUBTLE};
}}
"""
