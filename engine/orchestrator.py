"""OPC Board Engine — Orchestrator (protocol for Hermes agent).

This module defines the board meeting protocol. When the user requests a meeting,
the Hermes agent follows this protocol, using delegate_task to call perspective agents.

The orchestrator also provides utility functions for preparing and displaying results.
"""

from __future__ import annotations
import re
from datetime import datetime, timezone
from engine.models import (
    BOARD, AgentDef, Domain, Vote, Meeting, Verdict,
    TOPIC_VOTERS, DEFAULT_DOMAINS,
)
from engine.router import classify, get_voters, get_reference, format_summary
from engine.consensus import final_verdict
from engine.prompts import build_vote_prompt, build_reference_prompt

PASS_THRESHOLD = 6
MAX_BATCH_SIZE = 3  # delegate_task concurrent limit


def domain_emoji(d: Domain) -> str:
    return {"finance": "💰", "brand": "📱", "health": "🧬",
            "strategy": "🧠", "innovation": "🚀"}.get(d.value, "❓")


def format_meeting_plan(topic: str, context: dict | None = None) -> str:
    """Generate a human-readable meeting plan."""
    domains = classify(topic)
    voters = get_voters(domains)
    refs = get_reference(domains)
    lines = [
        f"═══ BOARD MEETING PLAN ═══",
        f"Topic: {topic}",
        "",
    ]
    if context:
        import json
        lines.append(f"Context: {json.dumps(context, ensure_ascii=False)}")
        lines.append("")

    lines.append(f"📋 Classified domains: {' '.join(domain_emoji(d) + d.value for d in domains)}")
    lines.append("")

    # Group voters by domain
    by_domain: dict[str, list[AgentDef]] = {}
    for a in voters:
        by_domain.setdefault(a.domain.value, []).append(a)
    lines.append("🗳️  VOTING TEAM:")
    for d_name, agents in by_domain.items():
        e = domain_emoji(Domain(d_name))
        names = ", ".join(f"{a.name} ({a.role})" for a in agents)
        lines.append(f"  {e} {d_name}: {names}")
    lines.append("")

    if refs:
        lines.append("🗣️  REFERENCE ONLY:")
        for a in refs:
            lines.append(f"  ・{a.name} ({a.role}) — gives reference opinion")
    lines.append("")

    lines.append(f"Scope: {len(voters)} voting + {len(refs)} reference = "
                 f"{len(voters) + len(refs)}/{len(BOARD)} advisors")
    return "\n".join(lines)


def format_vote_table(votes: list[Vote], title: str = "RESULTS") -> str:
    """Format votes as a readable table."""
    lines = [f"═══ {title} ═══", ""]
    header = f"{'Agent':22s} {'Role':6s} {'Score':6s}  {'Concerns'}"
    lines.append(header)
    lines.append("-" * 60)
    for v in sorted(votes, key=lambda x: -x.score):
        marker = "✅" if v.passed else "❌"
        concern = (v.key_concerns[0] if v.key_concerns else "-")[:40]
        lines.append(f"{marker} {v.agent_name:22s} {v.role:6s} "
                     f"{v.score:>2d}/10  {concern}")
    return "\n".join(lines)


def format_verdict(meeting: Meeting) -> str:
    """Format the final verdict."""
    v = meeting.final_verdict.value.upper()
    style = "✅ PASSED" if meeting.final_verdict == Verdict.PASSED else "❌ FAILED"
    return (
        f"\n{'='*50}\n"
        f"  FINAL VERDICT: {style}\n"
        f"  Topic: {meeting.topic}\n"
        f"  Score: {meeting.final_score}/10\n"
        f"  Rounds: {len(meeting.rounds)}\n"
        f"  Time: {meeting.timestamp[:19]}\n"
        f"{'='*50}"
    )


# ── HERMES AGENT PROTOCOL ──────────────────────────────────
# When a user requests a board meeting, follow this protocol.
# The protocol uses delegate_task to call perspective agents.

PROTOCOL = """
## OPC BOARD MEETING PROTOCOL

When user says they want a board meeting (or asks a decision question):

### Step 1: Classify Topic
Use classify(topic) from engine.router to determine relevant domains.
Show the meeting plan to the user.

### Step 2: Call Voting Team (Parallel)
For each domain team in the voting team:
  Call delegate_task with MAX_BATCH_SIZE agents at a time.
  Each subagent gets:
    - skill/context that loads their perspective skill
    - build_vote_prompt(agent, topic, context, round_num=1)
  Collect structured JSON votes.

### Step 3: Tally
Use tally(votes, round_num=1) to check results.
If all_passed → Step 5 (verdict).
If dissent → Step 4 (re-vote).

### Step 4: Re-vote (if needed)
Build dissent brief from dissenters.
Call delegate_task again for dissenters with round_num=2.
Collect revised votes, replace in the round.

### Step 5: Final Verdict
Compute final_verdict.
Show formatted results to user.

### Step 6: Save
Save meeting record.
If result passed and has action items, offer to create cron jobs.

### Topic routing rules:
- investment/finance topics → FINANCE + STRATEGY + INNOVATION
- health topics → HEALTH + FINANCE (for budget impact)
- brand/marketing → BRAND
- strategy/career → STRATEGY + FINANCE
- product/tech → INNOVATION + BRAND
- general business → call all domains
"""

if __name__ == "__main__":
    # Test the meeting plan display
    test_topics = [
        "定投5000块一个月，买QQQM还是SPY",
        "想做一个个人品牌自媒体账号，从0开始",
        "每天睡6小时，怎么优化睡眠质量",
        "35岁想转行学编程，来得及吗",
        "要不要ALL IN做AI创业",
    ]
    for t in test_topics:
        print(format_meeting_plan(t))
        print()