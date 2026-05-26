"""OPC Board Engine — Prompt templates for delegate_task calls."""

from __future__ import annotations
from engine.models import AgentDef


def build_vote_prompt(
    agent: AgentDef,
    topic: str,
    context: dict,
    round_num: int = 1,
    dissent_brief: str | None = None,
) -> str:
    """Build the prompt for a single perspective agent vote."""

    ctx_str = _fmt_context(context)

    prompt = (
        f"## Role: {agent.name} ({agent.role})\n"
        f"You are {agent.name}. Use your perspective skill (loaded) to analyze this topic.\n\n"
        f"## Decision Required\n"
        f"Topic: {topic}\n"
        + (f"Context: {ctx_str}\n" if ctx_str else "\n")
    )

    if round_num == 1:
        prompt += "This is the FIRST round. Give your honest assessment without hesitation.\n\n"
    else:
        prompt += (
            f"This is ROUND {round_num} re-vote.\n\n"
            f"**Dissent from prior round:**\n"
            f"{dissent_brief}\n\n"
            "Re-examine: have these concerns been addressed? "
            "If you accept them, adjust your score. "
            "If you disagree, state specifically why.\n\n"
        )

    prompt += _vote_output_format()
    return prompt


def build_reference_prompt(
    agent: AgentDef,
    topic: str,
    context: dict,
) -> str:
    """Build prompt for non-voting reference opinion."""
    ctx_str = _fmt_context(context)
    return (
        f"## Role: {agent.name} ({agent.role})\n"
        f"You are {agent.name}. The topic below is outside your core domain.\n"
        f"Provide your reference opinion based on your general philosophy.\n\n"
        f"## Reference Opinion\n"
        f"Topic: {topic}\n"
        + (f"Context: {ctx_str}\n" if ctx_str else "\n") +
        "Output **strict JSON** (no markdown):\n"
        '{"analysis": "<2-3 sentences from your perspective>", '
        '"agreement": <1-10 how much you agree with the proposal>, '
        '"concerns": ["..."], "advice": "..."}'
    )


def _vote_output_format() -> str:
    return (
        "\n---\n"
        "Output **strict JSON only** (no markdown, no extra text):\n"
        '{"score": <1-10 integer>, '
        '"reasoning": "<3-5 sentences from your perspective>", '
        '"key_concerns": ["<first concern>", "<second concern>"], '
        '"conditions": ["<what must be true for you to raise your score>"]}\n'
        "Score 1-10. 6+ = pass. Be specific, concrete, and data-driven."
    )


def _fmt_context(ctx: dict) -> str:
    if not ctx:
        return ""
    import json
    return json.dumps(ctx, ensure_ascii=False, indent=2)[:500]


def build_delegate_context(agent: AgentDef, prompt: str, skill_name: str) -> dict:
    """Build the context dict for delegate_task call to a subagent."""
    return {
        "goal": f"Act as {agent.name} ({agent.role}) on the OPC Board and vote on the topic with JSON output.",
        "context": f"SKILL to load: {skill_name}\n\n{prompt}",
        "toolsets": ["web", "terminal"] if agent.toolsets else [],
    }