"""
Main CLI entry point for commix.
"""
import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from typing_extensions import Annotated

from .generator import CommitGenerator
from .config import Config
from .git_utils import GitUtils

app = typer.Typer(
    name="commix",
    help="🤖 AI-Powered Smart Git Commit Assistant",
    add_completion=False,
)
console = Console()

# Version info
VERSION = "0.1.0"


@app.command()
def main(
    provider: Annotated[
        Optional[str],
        typer.Option(
            "--provider",
            "-p",
            help="AI provider to use (openai/claude/ollama)",
        ),
    ] = None,
    lang: Annotated[
        Optional[str],
        typer.Option(
            "--lang",
            "-l",
            help="Commit message language (en/zh/ja/ko)",
        ),
    ] = None,
    emoji: Annotated[
        bool,
        typer.Option(
            "--emoji",
            "-e",
            help="Enable gitmoji support",
        ),
    ] = False,
    interactive: Annotated[
        bool,
        typer.Option(
            "--interactive",
            "-i",
            help="Interactive mode",
        ),
    ] = False,
    commit: Annotated[
        bool,
        typer.Option(
            "--commit",
            "-c",
            help="Generate and create commit automatically",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            "-n",
            help="Preview without committing",
        ),
    ] = False,
    staged: Annotated[
        bool,
        typer.Option(
            "--staged",
            "-s",
            help="Only analyze staged changes",
        ),
    ] = False,
    batch: Annotated[
        bool,
        typer.Option(
            "--batch",
            "-b",
            help="Batch commit mode for large changes",
        ),
    ] = False,
):
    """
    Generate intelligent commit messages using AI.
    """
    try:
        # Load configuration
        config = Config()
        if provider:
            config.set("provider", provider)
        if lang:
            config.set("commit.language", lang)
        if emoji:
            config.set("gitmoji.enabled", True)

        # Check git repository
        if not GitUtils.is_git_repo():
            console.print("[red]Error: Not a git repository[/red]")
            raise typer.Exit(1)

        # Check for changes
        changes = GitUtils.get_diff(staged_only=staged)
        if not changes.strip():
            console.print("[yellow]No changes found to commit[/yellow]")
            return

        # Generate commit message
        generator = CommitGenerator(config)
        result = generator.generate(
            diff=changes,
            interactive=interactive,
            batch=batch,
        )

        if result:
            if dry_run:
                console.print(Panel(result, title="📝 Commit Message Preview"))
            elif commit or interactive:
                # Interactive mode - let user confirm
                confirm = typer.confirm(
                    f"\n[bold]Create commit with this message?[/bold]",
                    default=True,
                )
                if confirm:
                    GitUtils.commit(result)
                    console.print("[green]✓ Commit created successfully![/green]")
                else:
                    console.print("[yellow]Commit cancelled[/yellow]")
            else:
                console.print(Panel(result, title="📝 Generated Commit Message"))
                console.print("\n[dim]Tip: Use --commit to create commit automatically[/dim]")
        else:
            console.print("[red]Failed to generate commit message[/red]")
            raise typer.Exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        raise typer.Exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def commit(
    message: str = typer.Argument(..., help="Commit message"),
    amend: bool = typer.Option(False, "--amend", help="Amend the last commit"),
):
    """Create a commit with the given message."""
    try:
        if not GitUtils.is_git_repo():
            console.print("[red]Error: Not a git repository[/red]")
            raise typer.Exit(1)

        GitUtils.commit(message, amend=amend)
        console.print(f"[green]✓ Committed: {message[:50]}...[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def config_cmd(
    action: str = typer.Argument(..., help="Action: get/set/list"),
    key: Optional[str] = typer.Argument(None, help="Config key"),
    value: Optional[str] = typer.Argument(None, help="Config value"),
):
    """Manage configuration."""
    config = Config()

    if action == "list":
        table = Table(title="Current Configuration")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")

        for key, val in config.data.items():
            if isinstance(val, dict):
                for sub_key, sub_val in val.items():
                    table.add_row(f"{key}.{sub_key}", str(sub_val))
            else:
                table.add_row(key, str(val))
        console.print(table)

    elif action == "get":
        if key:
            val = config.get(key)
            console.print(f"[cyan]{key}[/cyan] = [green]{val}[/green]")
        else:
            console.print("[red]Please specify a key[/red]")

    elif action == "set":
        if key and value:
            config.set(key, value)
            console.print(f"[green]✓ Set {key} = {value}[/green]")
        else:
            console.print("[red]Please specify key and value[/red]")

    else:
        console.print(f"[red]Unknown action: {action}[/red]")


@app.command()
def providers():
    """List available AI providers."""
    table = Table(title="Available AI Providers")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Description", style="dim")

    providers_info = [
        ("openai", "✓ Configured", "OpenAI GPT models"),
        ("claude", "⚠ Not configured", "Anthropic Claude models"),
        ("ollama", "⚠ Not configured", "Local Ollama models"),
    ]

    for name, status, desc in providers_info:
        table.add_row(name, status, desc)

    console.print(table)


@app.command()
def version():
    """Show version information."""
    console.print(f"[bold]commix[/bold] version [green]{VERSION}[/green]")
    console.print("[dim]AI-Powered Smart Git Commit Assistant[/dim]")


if __name__ == "__main__":
    app()
