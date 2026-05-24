"""Memory layer — persists agent decisions between rounds."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

MEMORY_DIR = Path(__file__).parent.parent / "memory"
MEETING_LOG = MEMORY_DIR / "meetings.jsonl"
AGENT_MEMORY = MEMORY_DIR / "agent_memory.json"


@dataclass
class AgentVote:
    agent_id: str
    agent_name: str
    role: str
    crew: str
    score: int           # 1-10
    reasoning: str       # why this score
    key_concerns: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)  # pass conditions / caveats
    strengths: list[str] = field(default_factory=list)
    raw_output: str = ""         # full LLM output
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def passed(self) -> bool:
        return self.score >= 6


@dataclass
class MeetingRecord:
    id: str
    topic: str
    context: dict[str, Any]
    votes: list[AgentVote]
    final_score: float | None = None
    final_verdict: str = "pending"        # pending | passed | failed | revised
    revision_round: int = 0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    executive_summary: str = ""
    action_items: list[dict] = field(default_factory=list)

    @property
    def avg_score(self) -> float:
        return round(sum(v.score for v in self.votes) / max(len(self.votes), 1), 2)

    @property
    def all_passed(self) -> bool:
        return all(v.passed for v in self.votes)

    @property
    def dissenters(self) -> list[AgentVote]:
        return [v for v in self.votes if not v.passed]


class MeetingMemory:
    """Append-only meeting store.

    After each board meeting:
    1. Individual votes written to agent_memory.json (role-scoped)
    2. Full meeting record appended to meetings.jsonl
    """

    def __init__(self, memory_dir: Path | None = None):
        self.memory_dir = memory_dir or MEMORY_DIR
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self._agent_memory: dict[str, dict] = {}
        self._load_agent_memory()

    def _load_agent_memory(self) -> None:
        if AGENT_MEMORY.exists():
            try:
                self._agent_memory = json.loads(AGENT_MEMORY.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self._agent_memory = {}

    def _save_agent_memory(self) -> None:
        AGENT_MEMORY.write_text(
            json.dumps(self._agent_memory, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def record_vote(self, vote: AgentVote) -> None:
        """Persist a single agent's vote into long-term role memory."""
        entry = {
            "timestamp": vote.timestamp,
            "topic_hash": vote.agent_id,
            "score": vote.score,
            "reasoning": vote.reasoning,
            "key_concerns": vote.key_concerns,
            "conditions": vote.conditions,
            "raw_output": vote.raw_output[:2000],  # cap at 2K chars
        }
        self._agent_memory.setdefault(vote.agent_id, []).append(entry)
        self._save_agent_memory()

    def get_agent_history(self, agent_id: str, limit: int = 10) -> list[dict]:
        return self._agent_memory.get(agent_id, [])[-limit:]

    def save_meeting(self, record: MeetingRecord) -> Path:
        """Append meeting record to append-only log."""
        line = json.dumps(asdict(record), ensure_ascii=False, default=str)
        with MEETING_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        return MEETING_LOG

    def load_meetings(self, limit: int = 20) -> list[dict]:
        """Read the last N meetings from the log."""
        if not MEETING_LOG.exists():
            return []
        lines = MEETING_LOG.read_text(encoding="utf-8").strip().splitlines()
        return [json.loads(l) for l in lines[-limit:] if l.strip()]

    def get_last_meeting_on(self, topic_keyword: str) -> dict | None:
        for m in reversed(self.load_meetings(100)):
            if topic_keyword.lower() in m.get("topic", "").lower():
                return m
        return None
