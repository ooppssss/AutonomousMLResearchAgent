"""The automl terminal user interface."""

from __future__ import annotations

import os
import subprocess

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input

from . import __version__
from .commands import get_registry
from .theme import APP_CSS
from .widgets import Conversation, LogoBanner, PromptInput, StatusBar

WELCOME = (
    "Welcome. Type a message, or use /commands and !shell.\n"
    "Nothing is wired to a model yet — this is the CLI shell."
)


class AutomlApp(App):
    """Full-screen, opencode-style interface for the research agent."""

    CSS = APP_CSS
    TITLE = "automl"
    SUB_TITLE = "autonomous ML research agent"
    ENABLE_COMMAND_PALETTE = False

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+l", "clear_log", "Clear"),
        Binding("f1", "help", "Help"),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.version = __version__
        self.cwd = os.getcwd()
        self.registry = get_registry()

    # -- layout -------------------------------------------------------------
    def compose(self) -> ComposeResult:
        yield LogoBanner(self.cwd)
        yield Conversation()
        yield PromptInput(self.registry.suggestions())
        yield StatusBar(self.cwd)

    def on_mount(self) -> None:
        self.conversation.add_system(WELCOME)
        self.query_one(PromptInput).focus()

    # -- helpers ------------------------------------------------------------
    @property
    def conversation(self) -> Conversation:
        return self.query_one(Conversation)

    def write_user(self, message: str) -> None:
        self.conversation.add_user(message)

    def write_agent(self, message: str) -> None:
        self.conversation.add_agent(message)

    def write_system(self, message: str) -> None:
        self.conversation.add_system(message)

    def write_error(self, message: str) -> None:
        self.conversation.add_error(message)

    def show_help(self) -> None:
        from .theme import help_panel

        self.conversation.write(help_panel(self.registry.all()))

    def clear_conversation(self) -> None:
        self.conversation.clear()

    # -- input handling -----------------------------------------------------
    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        if not raw:
            return
        if raw.startswith("/"):
            self._handle_command(raw)
        elif raw.startswith("!"):
            self.write_user(raw)
            self._run_shell(raw[1:].strip())
        else:
            self.write_user(raw)
            self.write_system("No agent is wired yet. Type /help for commands.")

    def _handle_command(self, raw: str) -> None:
        self.write_user(raw)
        parts = raw[1:].strip().split()
        if not parts:
            return
        name, args = parts[0], parts[1:]
        command = self.registry.resolve(name)
        if command is None:
            self.write_error(f"Unknown command '/{name}'. Type /help for commands.")
            return
        try:
            command.handler(self, args)
        except Exception as exc:  # noqa: BLE001 - surface any command failure
            self.write_error(f"/{name} failed: {exc}")

    # -- shell integration --------------------------------------------------
    @work(thread=True, group="shell")
    def _run_shell(self, command: str) -> None:
        if not command:
            self.call_from_thread(self.write_system, "Nothing to run.")
            return
        try:
            completed = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
            )
            output = (completed.stdout or "") + (completed.stderr or "")
            self.call_from_thread(
                self._render_shell,
                command,
                output.strip(),
                completed.returncode,
            )
        except Exception as exc:  # noqa: BLE001
            self.call_from_thread(
                self.conversation.add_tool,
                f"! {command}",
                str(exc),
                ok=False,
            )

    def _render_shell(self, command: str, output: str, returncode: int) -> None:
        body = output or "(no output)"
        self.conversation.add_tool(
            f"! {command}  (exit {returncode})",
            body,
            ok=returncode == 0,
        )

    # -- actions ------------------------------------------------------------
    def action_clear_log(self) -> None:
        self.clear_conversation()

    def action_help(self) -> None:
        self.show_help()
