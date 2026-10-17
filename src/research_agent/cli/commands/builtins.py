"""Built-in slash commands.

These are intentionally minimal — they only touch the TUI. Add your own
commands in sibling modules and they will be picked up automatically.
"""

from __future__ import annotations

from .registry import registry


@registry.command("help", description="Show the available commands.", aliases=("h", "?"))
def _help(app, args: list[str]) -> None:
    app.show_help()


@registry.command("clear", description="Clear the conversation.", aliases=("cls",))
def _clear(app, args: list[str]) -> None:
    app.clear_conversation()


@registry.command("version", description="Show the CLI version.", aliases=("v",))
def _version(app, args: list[str]) -> None:
    app.write_system(f"automl {app.version}")


@registry.command("exit", description="Exit the CLI.", aliases=("quit", "q"))
def _exit(app, args: list[str]) -> None:
    app.exit()
