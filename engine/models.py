"""OPC Board Engine — Data models for the universal board platform."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class Domain(str, Enum):
    FINANCE = "finance"
    BRAND = "brand"
    HEALTH = "health"
    STRATEGY = "strategy"
    INNOVATION = "innovation"


class Verdict(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    REVISED = "revised"


@dataclass
class AgentDef:
    id: str
    name: str
    role: str
    domain: Domain
    skill_name: str          # Hermes skill to load
    voting_weight: int = 1
    toolsets: list[str] = field(default_factory=list)

    @property
    def is_cfo(self) -> bool:
        return self.role == "CFO"


@dataclass
class Vote:
    agent_id: str
    agent_name: str
    role: str
    domain: Domain
    score: int                # 1-10
    reasoning: str = ""
    key_concerns: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    round: int = 1

    @property
    def passed(self) -> bool:
        return self.score >= 6


@dataclass
class RoundResult:
    round: int
    votes: list[Vote]
    avg_score: float = 0.0
    all_passed: bool = False
    dissenters: list[Vote] = field(default_factory=list)
    verdict: Verdict = Verdict.FAILED


@dataclass
class Meeting:
    id: str
    topic: str
    context: dict
    rounds: list[list[Vote]] = field(default_factory=list)
    final_score: float = 0.0
    final_verdict: Verdict = Verdict.FAILED
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def all_votes(self) -> list[Vote]:
        return self.rounds[-1] if self.rounds else []


# ── Agent Registry ──────────────────────────────────────────

BOARD: list[AgentDef] = [
    AgentDef("naval",  "Naval Ravikant",     "CFO", Domain.FINANCE,   "naval-perspective"),
    AgentDef("buffett","Warren Buffett",     "CFO", Domain.FINANCE,   "buffett-perspective"),
    AgentDef("duan",   "Duan Yongping",      "CFO", Domain.FINANCE,   "duan-perspective"),
    AgentDef("trump",  "Donald Trump",       "CBO", Domain.BRAND,     "trump-perspective"),
    AgentDef("dan_koe","Dan Koe",            "CMO", Domain.BRAND,     "dan-koe-perspective"),
    AgentDef("bryan",  "Bryan Johnson",      "CHO", Domain.HEALTH,    "bryan-johnson-perspective"),
    AgentDef("huberman","Andrew Huberman",   "CHO", Domain.HEALTH,    "huberman-perspective"),
    AgentDef("zhang",  "Zhang Xuedong",      "CSO", Domain.STRATEGY,  "zhangxuefeng-perspective"),
    AgentDef("lidang", "Lidangzzz",          "COO", Domain.STRATEGY,  "lidangzzz-perspective"),
    AgentDef("musk",   "Elon Musk",          "CVO", Domain.INNOVATION,"elon-musk-perspective"),
]

# Topic → voting team mapping
TOPIC_VOTERS: dict[str, list[Domain]] = {
    "investment": [Domain.FINANCE, Domain.STRATEGY, Domain.INNOVATION],
    "finance":    [Domain.FINANCE, Domain.STRATEGY, Domain.INNOVATION],
    "health":     [Domain.HEALTH, Domain.FINANCE],
    "brand":      [Domain.BRAND],
    "marketing":  [Domain.BRAND],
    "strategy":   [Domain.STRATEGY, Domain.FINANCE, Domain.INNOVATION],
    "career":     [Domain.STRATEGY, Domain.FINANCE],
    "operation":  [Domain.STRATEGY],
    "product":    [Domain.INNOVATION, Domain.BRAND],
    "business":   [Domain.FINANCE, Domain.STRATEGY, Domain.BRAND, Domain.INNOVATION],
}

# Default: call all domains
DEFAULT_DOMAINS = list(Domain)