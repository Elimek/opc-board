#!/usr/bin/env python3
"""
OPC Board — CLI v2
One-Person Company Operating System, Crew-powered edition.

Usage:
    python opc.py                          # Interactive menu
    python opc.py board                    # Start a new board meeting (prompts for topic)
    python opc.py board --topic "..."      # Non-interactive: topic as argument
    python opc.py board --topic "..." --context '{"amount":1000}'
    python opc.py votes [meeting_id]       # Print DCA July plan voting results
    python opc.py agents                   # List all 10 board members
    python opc.py history [N]              # Last N meetings
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

sys.path.insert(0, str(Path(__file__).parent))
from crews.coordinator import BoardCoordinator
from crews.memory import MeetingMemory
from crews.registry_loader import load_registry, list_all_agents

app = typer.Typer(
    name="opc",
    help="🏢 OPC Board — Your One-Person Company Board of Directors",
    no_args_is_help=False,
)
console = Console()


# ────────────────────────────────────────────────────────────────────────────
# helpers
# ────────────────────────────────────────────────────────────────────────────

def _print_header(text: str):
    console.print(f"\n[bold cyan]{'═'*60}[/bold cyan]")
    console.print(f"[bold cyan]{text.center(60)}[/bold cyan]")
    console.print(f"[bold cyan]{'═'*60}[/bold cyan]\n")


def _result_table(result: dict) -> None:
    t = Table(title=f"Meeting: {result['topic']}", show_header=True, header_style="bold magenta")
    t.add_column("Agent", style="cyan", min_width=20)
    t.add_column("Role", min_width=12)
    t.add_column("Score", justify="center")
    t.add_column("Round", justify="center")
    t.add_column("Concerns", min_width=30)
    t.add_column("Pass?", justify="center")

    for v in result["vote_detail"]:
        passed = "✅" if v["score"] >= 6 else "❌"
        score_style = "green" if v["score"] >= 6 else "red"
        t.add_row(
            v["agent"],
            v["role"],
            f"[{score_style}]{v['score']}/10[/{score_style}]",
            str(v.get("round", 1)),
            "; ".join(v.get("key_concerns", [])[:2]) or "-",
            passed,
        )
    console.print(t)

    # Summary line
    verdict = result["verdict"]
    verdict_style = "bold green" if verdict == "passed" else "bold red"
    console.print(f"\n[{verdict_style}]Final Verdict: {verdict.upper()}[/{verdict_style}]  "
                  f"Avg Score: [bold]{result['final_score']}/10[/bold]  "
                  f"Rounds: {result['rounds']}\n")


# ────────────────────────────────────────────────────────────────────────────
# commands
# ────────────────────────────────────────────────────────────────────────────

@app.command()
def board(
    topic: str = typer.Argument(None, help="The decision topic to vote on"),
    context: str = typer.Option("{}", "--context", "-c", help="JSON context for the meeting"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output raw JSON"),
):
    """Start a board meeting — gather 10 agent votes and issue verdict."""
    ctx = json.loads(context) if context else {}

    if not topic:
        topic = typer.prompt("What's the topic or decision for today's board meeting?")
        if not topic:
            console.print("[yellow]No topic provided. Aborting.[/yellow]")
            raise typer.Exit(1)

    console.print(f"\n[yellow]Calling board meeting:[/yellow] {topic}")
    console.print(f"[dim]Context: {json.dumps(ctx, ensure_ascii=False)[:200]}[/dim]\n")
    console.print("[yellow]Agents are deliberating...[/yellow]\n")

    coord = BoardCoordinator()
    result = coord.start_meeting(topic, ctx)

    if json_output:
        console.print(JSON(json.dumps(result, indent=2, ensure_ascii=False, default=str)))
    else:
        _result_table(result)
        console.print(Panel(
            result.get("execution", {}).get("executive_summary", ""),
            title="Executive Summary",
            border_style="cyan",
        ))
        if result["execution"].get("action_items"):
            console.print("\n[bold]Action Items:[/bold]")
            for item in result["execution"]["action_items"]:
                console.print(f"  [{item.get('priority','-').upper()}] {item.get('owner','?')}: {item.get('action','')}")
        if result["execution"].get("suggested_cron"):
            console.print("\n[bold]Suggested cron jobs:[/bold]")
            for cmd in result["execution"]["suggested_cron"]:
                console.print(f"  {cmd}")


@app.command()
def agents():
    """List all 10 board members."""
    _print_header("OPC BOARD — 10 DIRECTORS")
    t = Table(show_header=True, header_style="bold cyan")
    t.add_column("ID", min_width=10)
    t.add_column("Name", style="cyan", min_width=22)
    t.add_column("Role", min_width=8)
    t.add_column("Crew", min_width=12)
    t.add_column("Tools", min_width=24)

    for a in list_all_agents():
        t.add_row(
            a["id"],
            a["name"],
            a["role"],
            a["crew"],
            ", ".join(a.get("toolsets", ["none"])),
        )
    console.print(t)


@app.command()
def history(n: int = typer.Option(10, "--limit", "-n", help="Last N meetings")):
    """Show recent board meetings."""
    mem = MeetingMemory()
    meetings = mem.load_meetings(limit=n)
    _print_header(f"RECENT BOARD MEETINGS (last {n})")
    if not meetings:
        console.print("[dim]No meetings on record yet.[/dim]")
        return
    t = Table(show_header=True, header_style="dim cyan")
    t.add_column("Date", min_width=12)
    t.add_column("ID", min_width=28)
    t.add_column("Topic", max_width=40)
    t.add_column("Score", justify="center")
    t.add_column("Verdict", justify="center")
    for m in reversed(meetings):
        verdict_style = {"passed": "green", "failed": "red", "revised": "yellow"}.get(
            m.get("final_verdict", ""), "white"
        )
        t.add_row(
            m.get("timestamp", "?")[:10],
            m.get("id", "?")[-20:],
            m.get("topic", "?")[:38],
            str(m.get("final_score", "?")),
            f"[{verdict_style}]{m.get('final_verdict', '?')}[/{verdict_style}]",
        )
    console.print(t)


@app.command()
def votes(topic_pattern: str = typer.Argument(None, help="Search pattern for topic")):
    """Show voting history for a specific topic."""
    import re
    mem = MeetingMemory()
    meetings = mem.load_meetings(200)
    if topic_pattern:
        meetings = [m for m in meetings if re.search(topic_pattern.lower(), m.get("topic", "").lower())]
    if not meetings:
        console.print(f"[dim]No meetings found matching '{topic_pattern}'.[/dim]")
        return
    for m in meetings:
        console.print(f"\n[cyan]── {m['topic']} ({m.get('final_verdict','?')}) " + 
                      f"score={m.get('final_score','?')}[/cyan]")
        for v in m.get("votes", []):
            style = "green" if v.get("score", 0) >= 6 else "red"
            console.print(f"  [{style}]{v.get('agent_name','?')}: {v.get('score',0)}/10 — "
                          f"{v.get('reasoning','')[:60]}[/{style}]")


if __name__ == "__main__":
    app()
