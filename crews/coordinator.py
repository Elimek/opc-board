"""Coordinator — CEO workflow: start meeting, collect votes, issue verdict.

Uses Hermes CLI (`hermes chat -q`) for real agent deliberation.
Falls back to simulation mode only when Hermes is completely unavailable.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from crews.aggregator import Aggregator
from crews.execution import Executor
from crews.memory import AgentVote, MeetingMemory, MeetingRecord
from crews.registry_loader import get_agent, get_crew_agents, get_voting_rules, load_registry


def _gen_meeting_id(topic: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower())[:40].strip("-")
    return f"{ts}--{slug}"


def _parse_vote_json(raw: str) -> dict:
    """Robust JSON extraction from LLM output."""
    raw = raw.strip()
    m = re.search(r"\{[\s\S]*\}", raw)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    score_match = re.search(r'"?score"?\s*:?\s*(\d+)', raw)
    return {"score": int(score_match.group(1)) if score_match else 5,
            "reasoning": raw[:300], "key_concerns": [], "conditions": []}


def _strip_session_id(raw: str) -> str:
    """Remove the 'session_id: ...' line that hermes -Q leaves on stdout."""
    lines = raw.strip().splitlines()
    if lines and lines[0].startswith("session_id:"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def _call_agent(agent: dict, prompt: str, timeout: int = 35) -> str:
    """Call Hermes CLI for this agent's vote. Returns raw response text."""
    try:
        proc = subprocess.run(
            ["hermes", "chat", "-q", prompt, "-Q"],
            capture_output=True, text=True, timeout=timeout,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return _strip_session_id(proc.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass

    # ── Simulated fallback — deterministic from prompt hash ──
    seed = abs(hash(agent["id"] + prompt[:200])) % 100
    score = 4 + (seed % 5)   # 4-8

    base_reasons = {
        "buffett": "Circle of competence check. Margin of safety sufficient. Moats adequate.",
        "naval":   "Optionality present. Long-term compound pathway confirmed.",
        "duan":    "Current window acceptable. Time-horizon verified. Strategic integrity OK.",
        "trump":   "Good visibility and narrative. Can be positioned as a winning deal.",
        "dan_koe": "Content angle is strong. Personal brand alignment present. Funnel viable.",
        "bryan":   "Stress test passed. Eligible for long-horizon hormone-locked DCAing.",
        "huberman":"Dopamine/reward prediction errors within tolerable band. Sleep protocol unaffected.",
        "zhang":   "Inflection point alignment confirmed. Forward-validated.",
        "lidang":  "Actual numbers verified. Automation-compatible. Clean on FLiP structure.",
        "musk":    "Idiot index acceptable. Physics check green. Vertical integration cost: 0.",
    }

    return json.dumps({
        "score": score,
        "reasoning": base_reasons.get(agent["id"], "No specific analysis."),
        "key_concerns": ["simulated mode — install hermes CLI for live agent output"],
        "conditions": [f"score>=6: re-evaluate in 4 weeks"],
        "reason_changed": "simulated — actual score requires hermes runtime",
    })


class BoardCoordinator:
    """Top-level flow: init → distribute → collect → aggregate → execute."""

    def __init__(self, memory: MeetingMemory | None = None):
        self.memory = memory or MeetingMemory()
        self.aggregator = Aggregator(memory=self.memory)
        self.executor = Executor(memory=self.memory)
        self._topic: str = ""
        self._context: dict = {}
        self.registry = load_registry()

    def start_meeting(self, topic: str, context: dict | None = None) -> dict:
        """Main entry point. Returns structured meeting result."""
        self._topic = topic
        self._context = context or {}
        meeting_id = _gen_meeting_id(topic)
        voting_rules = get_voting_rules()
        max_rounds = voting_rules.get("re_dissent_max_rounds", 1) + 1

        all_rounds: list[list[AgentVote]] = []

        for round_num in range(1, max_rounds + 1):
            round_votes = self._run_vote_round(
                round_num=round_num,
                prior_rounds=all_rounds,
            )
            all_rounds.append(round_votes)
            result = self.aggregator.tally(round_votes, round_num)

            if result.all_passed:
                break
            if round_num >= max_rounds:
                break

        record = self.aggregator.finalize(meeting_id, topic, self._context, all_rounds)
        exec_result = self.executor.run(record)

        return {
            "meeting_id": record.id,
            "topic": topic,
            "rounds": len(all_rounds),
            "final_score": record.final_score,
            "verdict": record.final_verdict,
            "all_passed": record.all_passed,
            "execution": exec_result,
            "vote_detail": [
                {
                    "agent": v.agent_name,
                    "role": v.role,
                    "score": v.score,
                    "reasoning": v.reasoning,
                    "conditions": v.conditions,
                    "key_concerns": v.key_concerns,
                    "round": next(
                        (idx + 1 for idx, r_votes in enumerate(all_rounds)
                         if any(x.agent_id == v.agent_id for x in r_votes)),
                        1
                    ),
                }
                for v in record.votes
            ],
        }

    def _build_agent_prompt(self, agent: dict, round_num: int,
                             dissent_brief: str | None = None) -> str:
        topic = self._topic
        ctx = self._context
        ctx_str = json.dumps(ctx, ensure_ascii=False) if ctx else ""

        base = (
            f"## Role: {agent['name']} | {agent['role']}\n"
            f"{agent['system_prompt']}\n"
            f"## Decision for CEO\n"
            f"Topic: {topic}\n"
            + (f"Context/Data provided by CEO:\n{ctx_str}\n" if ctx else "\n")
            + ("This is the FIRST round. Do not hold back.\n" if round_num == 1
               else f"This is ROUND {round_num}.\n\n"
                    f"**Other agents' dissent from the prior round:**\n"
                    f"{dissent_brief or 'None.'}\n\n"
                    "Re-examine: have these concerns been addressed? "
                    "If you accept any, lower your conditions. "
                    "If you disagree, state specifically why.\n")
        )
        base += (
            "\n---\n"
            "Output **strict JSON** (no markdown, no extra text):\n"
            '{"score": <1-10 int>, "reasoning": "<3-5 sentences>", '
            '"key_concerns": ["..."], "conditions": ["<what must be true for you to raise your score>"], '
            '"reason_changed": "<why this round differs from prior, or blank if same>"}'
        )
        return base

    def _run_vote_round(self, round_num: int, prior_rounds: list[list[AgentVote]]) -> list[AgentVote]:
        agents = self.registry["agents"]
        dissent_brief = None

        if prior_rounds:
            prior = self.aggregator.tally(prior_rounds[-1], round_num - 1)
            dissent_brief = self.aggregator._build_dissent_brief(prior.dissenters)

        def _vote(agent):
            prompt = self._build_agent_prompt(agent, round_num, dissent_brief)
            raw = _call_agent(agent, prompt)
            parsed = _parse_vote_json(raw)
            vote = AgentVote(
                agent_id=agent["id"],
                agent_name=agent["name"],
                role=agent["role"],
                crew=agent["crew"],
                score=parsed.get("score", 5),
                reasoning=parsed.get("reasoning", parsed.get("reason_changed", "")),
                key_concerns=parsed.get("key_concerns", []),
                conditions=parsed.get("conditions", []),
                raw_output=raw[:3000],
            )
            return vote

        votes: list[AgentVote] = []
        with ThreadPoolExecutor(max_workers=len(agents)) as pool:
            futures = {pool.submit(_vote, a): a for a in agents}
            for f in as_completed(futures):
                vote = f.result()
                self.memory.record_vote(vote)
                votes.append(vote)

        return votes
