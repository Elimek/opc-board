#!/usr/bin/env python3
"""OPC Board v3 — Universal multi-agent board platform CLI.

Usage:
    python opc.py                           # Interactive — explains the protocol
    python opc.py board "我的议题"           # Start a board meeting
    python opc.py plan "我的议题"            # Preview which advisors will be called
    python opc.py agents                    # List all 10 board members
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from engine.models import BOARD, Domain, TOPIC_VOTERS, Verdict
from engine.router import classify, get_voters, get_reference, format_summary
from engine.orchestrator import (
    format_meeting_plan,
    domain_emoji,
)

app = typer.Typer(no_args_is_help=False)
console = Console()


def _header(text: str):
    console.print(f"\n[bold cyan]{'═'*60}[/bold cyan]")
    console.print(f"[bold cyan]{text.center(60)}[/bold cyan]")
    console.print(f"[bold cyan]{'═'*60}[/bold cyan]")


# ────────────────────────────────────────────────────────────
# commands
# ────────────────────────────────────────────────────────────

@app.command()
def board(
    topic: str = typer.Argument(None, help="Decision topic"),
    context: str = typer.Option("{}", "--context", "-c", help="JSON context"),
):
    """Start a board meeting. The Hermes agent orchestrates via delegate_task."""
    ctx = _parse_context(context)

    if not topic:
        topic = typer.prompt("What's the topic or decision for today's board meeting?")
        if not topic:
            console.print("[yellow]No topic. Aborting.[/yellow]")
            raise typer.Exit(1)

    # Show meeting plan
    console.print(format_meeting_plan(topic, ctx))
    console.print()

    # --- NEW v3: The Hermes agent IS the orchestrator ---
    # When this message is sent to Hermes, the agent follows the PROTOCOL
    # in engine/orchestrator.py, using delegate_task to call perspective agents.
    console.print(Panel(
        "[bold green]v3 Engine ready[/bold green]\n\n"
        "Send this topic to Hermes as a chat message. "
        "The agent will:\n"
        "1. Classify the topic → determine domain\n"
        "2. Call relevant perspective advisors via delegate_task\n"
        "3. Collect votes → detect dissent → re-vote if needed\n"
        "4. Issue final verdict\n\n"
        "Or just type your question directly in the chat.",
        title="Next Step",
        border_style="green",
    ))


@app.command()
def plan(
    topic: str = typer.Argument(..., help="Topic to analyze"),
):
    """Preview which advisors will be called for a topic."""
    domains = classify(topic)
    voters = get_voters(domains)
    refs = get_reference(domains)

    _header("BOARD MEETING PLAN PREVIEW")
    console.print(f"\n[bold]Topic:[/bold] {topic}")
    console.print(f"[bold]Domains:[/bold] {' '.join(f'{domain_emoji(d)}{d.value}' for d in domains)}\n")

    # Voting team table
    t = Table(show_header=True, header_style="bold cyan", title="🗳️ Voting Team")
    t.add_column("Agent", style="cyan", min_width=22)
    t.add_column("Role", min_width=8)
    t.add_column("Domain", min_width=12)
    t.add_column("SKILL", min_width=22)
    for a in voters:
        t.add_row(a.name, a.role, a.domain.value, a.skill_name)
    console.print(t)

    # Reference table
    if refs:
        t2 = Table(show_header=True, header_style="dim cyan", title="🗣️ Reference Only")
        t2.add_column("Agent", style="dim", min_width=22)
        t2.add_column("Role", min_width=8)
        t2.add_column("Domain", min_width=12)
        for a in refs:
            t2.add_row(a.name, a.role, a.domain.value)
        console.print(f"\n")
        console.print(t2)

    console.print(f"\n[dim]Total: {len(voters)} voting + {len(refs)} reference = "
                  f"{len(voters) + len(refs)}/{len(BOARD)} advisors[/dim]")


@app.command()
def agents():
    """List all 10 board members with their SKILL sources."""
    _header("OPC BOARD — 10 DIRECTORS")

    t = Table(show_header=True, header_style="bold cyan")
    t.add_column("ID", min_width=10, style="dim")
    t.add_column("Name", style="cyan", min_width=22)
    t.add_column("Role", min_width=8)
    t.add_column("Domain", min_width=12)
    t.add_column("SKILL", min_width=24)

    for a in BOARD:
        t.add_row(a.id, a.name, a.role, domain_emoji(a.domain) + a.domain.value, a.skill_name)
    console.print(t)


@app.command()
def domains():
    """Show topic→domain routing rules."""
    _header("TOPIC ROUTING RULES")
    t = Table(show_header=True, header_style="bold cyan")
    t.add_column("Topic Keywords", min_width=16)
    t.add_column("→ Domains", min_width=30)
    t.add_column("Advisors", min_width=30)
    for keyword, doms in TOPIC_VOTERS.items():
        agents = [a.name for a in BOARD if a.domain in doms]
        t.add_row(
            keyword,
            ", ".join(d.value for d in doms),
            ", ".join(agents[:4]) + ("…" if len(agents) > 4 else ""),
        )
    console.print(t)

    console.print("\n[dim]Default (unclassified): all 10 advisors[/dim]")


# ────────────────────────────────────────────────────────────
# helpers
# ────────────────────────────────────────────────────────────

def _parse_context(ctx_str: str) -> dict:
    import json
    try:
        return json.loads(ctx_str) if ctx_str and ctx_str != "{}" else {}
    except json.JSONDecodeError:
        return {}


if __name__ == "__main__":
    app()