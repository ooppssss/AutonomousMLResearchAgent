"""Entry point for the automl CLI.

Running ``automl`` with no arguments launches the interactive TUI. Passing a
subcommand dispatches to a click command, so the same binary can be scripted:

    automl              # open the TUI
    automl --version    # print the version
    automl <command>    # run a subcommand (add your own below)
"""

from __future__ import annotations

import click

from . import __version__

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def run_tui() -> None:
    """Launch the Textual interface, importing it lazily."""
    try:
        from .app import AutomlApp
    except ImportError as exc:
        click.secho(f"automl could not start the TUI: {exc}", fg="red", err=True)
        click.secho(
            "Install the UI dependencies with:  pip install textual rich",
            fg="yellow",
            err=True,
        )
        raise SystemExit(1) from exc
    AutomlApp().run()


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(
    __version__,
    "-v",
    "--version",
    prog_name="automl",
    message="%(prog)s %(version)s",
)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """automl - an opencode-style terminal CLI for ML research agents.

    Run without a command to open the interactive interface.
    """
    if ctx.invoked_subcommand is None:
        run_tui()


def main() -> None:
    """Console-script / ``python -m`` entry point."""
    cli()


if __name__ == "__main__":
    main()
