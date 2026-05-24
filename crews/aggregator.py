"""Aggregator — collect votes, detect dissent, drive re-debate, issue final verdict."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from crews.memory import AgentVote, MeetingMemory, MeetingRecord
from crews.registry_loader import load_registry


@dataclass
class VoteResult:
    round: int
    votes: list[AgentVote]
    avg_score: float
    all_passed: bool
    dissenters: list[AgentVote]
    verdict: str  # "passed" | "failed" | "revised"


class Aggregator:
    """Orchestrates the multi-round voting process.

    Flow:
      1.  Collect initial votes from all agents
      2.  If all_passed → issue PASS verdict, persist meeting
      3.  If dissent → broadcast dissent reasons, collect revised votes (max 1 extra round)
      4.  Re-evaluate
      5.  If still failed → issue FAIL verdict, persist meeting with revision log
    """

    def __init__(self, memory: MeetingMemory | None = None):
        self.memory = memory or MeetingMemory()

    def _verdict_label(self, votes: list[AgentVote], round_num: int) -> str:
        if all(v.passed for v in votes):
            return "passed"
        if round_num >= 2:
            return "failed"
        return "revised"

    def _build_dissent_brief(self, dissenters: list[AgentVote]) -> str:
        lines = ["The following agents scored below the pass threshold (6/10):\n"]
        for d in dissenters:
            lines.append(
                f"  [{d.agent_name} ({d.role})]  scored {d.score}/10\n"
                + f"    Reasoning: {d.reasoning}\n"
                + (f"    Key concerns: {'; '.join(d.key_concerns)}\n" if d.key_concerns else "")
                + (f"    Required conditions: {'; '.join(d.conditions)}\n" if d.conditions else "")
            )
        lines.append(
            "\nPlease re-evaluate considering the above. "
            "If your score changes, explain what shifted. "
            "If it stays the same, state why the concerns are unaddressed. "
            "Output strict JSON with updated score and reasoning."
        )
        return "\n".join(lines)

    def tally(self, votes: list[AgentVote], round_num: int) -> VoteResult:
        avg = round(sum(v.score for v in votes) / max(len(votes), 1), 2)
        return VoteResult(
            round=round_num,
            votes=votes,
            avg_score=avg,
            all_passed=all(v.passed for v in votes),
            dissenters=[v for v in votes if not v.passed],
            verdict=self._verdict_label(votes, round_num),
        )

    def build_revision_prompt(self, topic: str, context: dict, dissent_brief: str) -> str:
        """Build the prompt for a revised voting round."""
        prior = self.memory.get_last_meeting_on(topic[:30])
        prior_summary = ""
        if prior:
            prior_summary = f"\n\nPrior meeting on this topic (score={prior.get('final_score','?')}, verdict={prior.get('final_verdict','?')}):\n{prior.get('executive_summary','')[:500]}"

        return (
            f"## Re-vote Round\n"
            f"Topic: {topic}\n"
            f"{prior_summary}\n\n"
            f"{dissent_brief}\n\n"
            f"---\n"
            f"Output JSON ONLY:\n"
            f'{{"score": <1-10 integer>, "reasoning": "<2-3 sentences>", '
            f'"key_concerns": ["..."], "conditions": ["..."], "reason_changed": "<why or why not your score changed>"}}'
        )

    def finalize(self, meeting_id: str, topic: str, context: dict,
                 all_vote_rounds: list[list[AgentVote]]) -> MeetingRecord:
        """Build and persist the final meeting record."""
        final_votes = all_vote_rounds[-1]
        final_result = self.tally(final_votes, len(all_vote_rounds))

        # Build executive summary
        if final_result.all_passed:
            self.exec_summary = (
                f"PASS — avg {final_result.avg_score}/10 across {len(final_votes)} agents. "
                f"No dissent. Decision executed."
            )
        else:
            self.exec_summary = (
                f"BLOCKED — avg {final_result.avg_score}/10. "
                f"Dissenters: {', '.join(d.agent_name for d in final_result.dissenters)}. "
                f"No conditions satisfied for auto-approval."
            )

        # Build action items
        action_items = []
        for v in final_votes:
            if v.conditions:
                for c in v.conditions:
                    action_items.append({
                        "owner": v.agent_name,
                        "role": v.role,
                        "action": c,
                        "status": "open",
                    })

        record = MeetingRecord(
            id=meeting_id,
            topic=topic,
            context=context,
            votes=final_votes,
            final_score=final_result.avg_score,
            final_verdict=final_result.verdict,
            revision_round=len(all_vote_rounds) - 1,
            executive_summary=self.exec_summary,
            action_items=action_items,
        )
        self.memory.save_meeting(record)
        return record
