"""Command package for the automl CLI.

Drop a new module in this folder and any ``@registry.command(...)`` defined in
it is discovered automatically the next time the registry is loaded.
"""

from __future__ import annotations

import importlib
import pkgutil

from .base import Command
from .registry import CommandRegistry, registry

_SKIP = {"base", "registry"}
_loaded = False


def load_commands() -> None:
    """Import every command module once so their decorators run."""
    global _loaded
    if _loaded:
        return
    _loaded = True
    for module in pkgutil.iter_modules(__path__):
        if module.name in _SKIP:
            continue
        importlib.import_module(f"{__name__}.{module.name}")


def get_registry() -> CommandRegistry:
    """Return the shared registry, loading command modules first."""
    load_commands()
    return registry


__all__ = [
    "Command",
    "CommandRegistry",
    "registry",
    "get_registry",
    "load_commands",
]
