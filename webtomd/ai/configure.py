"""Interactive --configure flow for first-time AI setup."""

from __future__ import annotations

import os
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

console = Console()

CONFIG_PATH = Path.home() / ".webtomdrc"

PROVIDERS = [
    ("anthropic", "Anthropic (Claude)", "ANTHROPIC_API_KEY"),
    ("openai", "OpenAI (GPT)", "OPENAI_API_KEY"),
    ("gemini", "Google Gemini", "GEMINI_API_KEY"),
    ("groq", "Groq (Llama)", "GROQ_API_KEY"),
    ("ollama", "Ollama (local, no key needed)", "OLLAMA_HOST"),
]


def run() -> None:
    """Launch the interactive AI provider configuration wizard."""
    console.print("\n[bold cyan]webtomd AI Setup[/bold cyan]\n")
    console.print("Choose your AI provider:\n")

    for i, (slug, label, _) in enumerate(PROVIDERS, 1):
        console.print(f"  [green]{i}[/green]) {label}")

    console.print()
    choice = Prompt.ask(
        "Enter number",
        choices=[str(i) for i in range(1, len(PROVIDERS) + 1)],
        default="1",
    )
    idx = int(choice) - 1
    slug, label, env_key = PROVIDERS[idx]

    if slug == "ollama":
        host = Prompt.ask("Ollama host", default="http://localhost:11434")
        _write_config(slug, env_key, host)
        console.print(f"\n[green]Done![/green] Configured [bold]{label}[/bold] at {host}")
    else:
        console.print(f"\n  Get your key at the {label} dashboard.")
        api_key = Prompt.ask(f"Paste your {label} API key")
        if not api_key.strip():
            console.print("[red]No key provided. Aborting.[/red]")
            return
        _write_config(slug, env_key, api_key.strip())
        console.print(f"\n[green]Done![/green] Configured [bold]{label}[/bold].")

    console.print("\n  Next steps:")
    console.print("    webtomd https://example.com --ai summarize")
    console.print("    webtomd https://example.com --ai tl;dr\n")


def _write_config(slug: str, env_key: str, value: str) -> None:
    """Persist provider choice to ~/.webtomdrc and set env var for current session."""
    os.environ[env_key] = value

    existing_lines: list[str] = []
    if CONFIG_PATH.exists():
        existing_lines = CONFIG_PATH.read_text(encoding="utf-8").splitlines()

    new_lines: list[str] = []
    for line in existing_lines:
        stripped = line.strip()
        if stripped.startswith("ai_provider") or stripped.startswith(env_key.lower()):
            continue
        new_lines.append(line)

    if new_lines and new_lines[-1].strip():
        new_lines.append("")

    new_lines.append(f'ai_provider = "{slug}"')

    if slug != "ollama":
        console.print(
            f"\n  [dim]Tip: For security, prefer setting {env_key} as an environment variable[/dim]"
            f"\n  [dim]rather than storing it in ~/.webtomdrc.[/dim]\n"
        )
    else:
        new_lines.append(f'ollama_host = "{value}"')

    CONFIG_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
