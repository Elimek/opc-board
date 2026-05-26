"""OPC Board Engine — Consensus engine.
Vote tallying, dissent detection, re-vote logic, final verdict."""

from __future__ import annotations
from engine.models import Vote, RoundResult, Verdict

PASS_THRESHOLD = 6      # minimum score to pass
MIN_PASS_RATE = 1.0     # all must pass (for strict mode)


def tally(votes: list[Vote], round_num: int) -> RoundResult:
    """Tally a round of votes."""
    if not votes:
        return RoundResult(round=round_num, votes=[])

    avg = round(sum(v.score for v in votes) / len(votes), 2)
    dissenters = [v for v in votes if not v.passed]
    all_pass = len(dissenters) == 0

    # Determine verdict
    if all_pass:
        verdict = Verdict.PASSED
    elif round_num >= 2:
        verdict = Verdict.FAILED
    else:
        verdict = Verdict.REVISED

    return RoundResult(
        round=round_num,
        votes=votes,
        avg_score=avg,
        all_passed=all_pass,
        dissenters=dissenters,
        verdict=verdict,
    )


def build_dissent_brief(dissenters: list[Vote]) -> str:
    """Build dissent brief for re-vote round."""
    lines = ["## Dissent Report — Round Failed", ""]
    lines.append(f"**{len(dissenters)} agent(s)** scored below {PASS_THRESHOLD}/10:\n")
    for d in dissenters:
        lines.append(f"### {d.agent_name} ({d.role}) — Score: {d.score}/10")
        if d.reasoning:
            lines.append(f"> {d.reasoning}")
        if d.key_concerns:
            lines.append(f"- Key concerns: {'; '.join(d.key_concerns)}")
        if d.conditions:
            lines.append(f"- Conditions to raise score: {'; '.join(d.conditions)}")
        lines.append("")
    lines.append("---")
    lines.append("Re-evaluate considering the above dissent. "
                 "If your score changes, explain what shifted. "
                 "If it stays the same, state why concerns remain unaddressed.")
    return "\n".join(lines)


def needs_revote(result: RoundResult) -> bool:
    """Check if a re-vote round is needed."""
    return not result.all_passed and result.round < 2


def final_verdict(all_rounds: list[list[Vote]]) -> dict:
    """Compute final verdict from all rounds."""
    if not all_rounds:
        return {"score": 0, "verdict": "failed", "rounds": 0}

    final_votes = all_rounds[-1]
    final = tally(final_votes, len(all_rounds))
    avg = final.avg_score
    all_pass = final.all_passed

    return {
        "score": avg,
        "verdict": "passed" if all_pass else "failed",
        "rounds": len(all_rounds),
        "all_passed": all_pass,
    }