"""OPC Board Engine v3 — Universal multi-agent board platform.

Usage:
    from engine import orchestrator as O
    result = O.run_meeting("Should I invest in QQQ?", {"amount": 1000})

The engine orchestrates perspective agents via delegate_task calls.
"""
from engine.models import BOARD, AgentDef, Domain, Vote, Meeting, Verdict
from engine.router import classify, get_voters, get_reference
from engine.consensus import tally, build_dissent_brief, needs_revote, final_verdict
from engine.prompts import build_vote_prompt, build_reference_prompt

__all__ = [
    "BOARD",
    "AgentDef",
    "Domain",
    "Vote",
    "Meeting",
    "Verdict",
    "classify",
    "get_voters",
    "get_reference",
    "tally",
    "build_dissent_brief",
    "needs_revote",
    "final_verdict",
    "build_vote_prompt",
    "build_reference_prompt",
]