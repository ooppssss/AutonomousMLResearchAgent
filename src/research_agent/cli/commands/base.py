"""The shape of a slash command."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:  # pragma: no cover - typing only
    from ..app import AutomlApp

# Every command handler receives the running app plus the raw argument list.
CommandHandler = Callable[["AutomlApp", list[str]], None]


@dataclass
class Command:
    """A single, dispatchable slash command."""

    name: str
    handler: CommandHandler
    description: str = ""
    usage: str = ""
    aliases: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.usage:
            self.usage = f"/{self.name}"
