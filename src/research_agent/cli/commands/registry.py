"""A tiny registry that maps slash commands (and their aliases) to handlers."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from .base import Command, CommandHandler


class CommandRegistry:
    """Holds every registered command and resolves aliases."""

    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}
        self._aliases: dict[str, str] = {}

    # -- registration -------------------------------------------------------
    def register(self, command: Command) -> Command:
        if command.name in self._commands:
            raise ValueError(f"Command '/{command.name}' is already registered.")
        self._commands[command.name] = command
        for alias in command.aliases:
            if alias in self._aliases or alias in self._commands:
                raise ValueError(f"Alias '{alias}' is already in use.")
            self._aliases[alias] = command.name
        return command

    def command(
        self,
        name: str,
        description: str = "",
        aliases: Iterable[str] = (),
        usage: str = "",
    ) -> Callable[[CommandHandler], CommandHandler]:
        """Decorator used by command modules to register a handler."""

        def decorator(handler: CommandHandler) -> CommandHandler:
            self.register(
                Command(
                    name=name,
                    handler=handler,
                    description=description,
                    usage=usage,
                    aliases=tuple(aliases),
                )
            )
            return handler

        return decorator

    # -- lookup -------------------------------------------------------------
    def resolve(self, name: str) -> Command | None:
        key = self._aliases.get(name, name)
        return self._commands.get(key)

    def all(self) -> list[Command]:
        return sorted(self._commands.values(), key=lambda command: command.name)

    def suggestions(self) -> list[str]:
        items: list[str] = []
        for command in self.all():
            items.append(f"/{command.name}")
            items.extend(f"/{alias}" for alias in command.aliases)
        return items

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and self.resolve(name) is not None

    def __len__(self) -> int:
        return len(self._commands)


# Shared registry populated by importing the command modules.
registry = CommandRegistry()
