"""Execution engine — persist decisions, trigger follow-up actions."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from crews.memory import MeetingMemory, MeetingRecord

EXECUTION_LOG = Path(__file__).parent.parent / "memory" / "execution_log.jsonl"


@dataclass
class ActionItem:
    owner_agent: str
    role: str
    action: str
    priority: str = "medium"    # high / medium / low
    deadline: str | None = None
    status: str = "open"

    def to_dict(self) -> dict:
        return {
            "owner": self.owner_agent,
            "action": self.action,
            "priority": self.priority,
            "deadline": self.deadline,
            "status": self.status,
        }


class Executor:
    """Turns decisions into persisted action items and follow-up tasks."""

    def __init__(self, memory: MeetingMemory | None = None):
        self.memory = memory or MeetingMemory()

    # ─── decision persistence ───────────────────────────────────────────────

    def persist_decision(self, record: MeetingRecord) -> Path:
        """Write the meeting decision summary to the summary file."""
        summary_path = Path(record.context.get("summary_dir", "meetings/")) / f"{record.id}.md"
        summary_path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            f"# Board Meeting: {record.topic}\n",
            f"**Date:** {record.timestamp}",
            f"**Final Verdict:** {record.final_verdict.upper()}",
            f"**Avg Score:** {record.final_score}/10\n",
            "---\n",
            "## Executive Summary\n",
            record.executive_summary,
            "\n\n## Votes\n",
            "| Agent | Role | Score | Pass? |",
            "|-------|------|-------|-------|",
        ]
        for v in record.votes:
            lines.append(f"| {v.agent_name} | {v.role} | {v.score}/10 | {'✅' if v.passed else '❌'} |")

        if record.action_items:
            lines += ["\n\n## Action Items\n", "| Owner | Action | Priority |", "|-------|--------|----------|"]
            for a in record.action_items:
                lines.append(f"| {a['owner']} | {a['action']} | {a.get('priority','-')} |")

        summary_path.write_text("\n".join(lines), encoding="utf-8")
        return summary_path

    # ─── execution log ──────────────────────────────────────────────────────

    def log_execution(self, record: MeetingRecord, summary_path: Path) -> None:
        """Append to append-only execution log for audit trail."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "meeting_id": record.id,
            "topic": record.topic,
            "verdict": record.final_verdict,
            "avg_score": record.final_score,
            "action_items_count": len(record.action_items),
            "summary_path": str(summary_path),
        }
        with EXECUTION_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    # ─── cron / follow-up ───────────────────────────────────────────────────

    def schedule_cron(self, record: MeetingRecord) -> list[str]:
        """Return cron commands for follow-up tasks when verdict is 'passed'."""
        if record.final_verdict != "passed":
            return []

        overdue: list[str] = []
        for item in record.action_items:
            if item["status"] == "open":
                # Suggest what cron the user might want
                severity = item.get("priority", "medium")
                cron_cmd = (
                    f"cronjob(action='create', job_id='followup-{record.id}-{item['owner'].lower()}', "
                    f"schedule='0 9 * * 1', prompt='Follow up on board meeting {record.id}: "
                    f"{item['action']}')"
                )
                if severity == "high":
                    overdue.append(f"[HIGH] {cron_cmd}")
                else:
                    overdue.append(f"[MEDIUM] {cron_cmd}")
        return overdue

    # ─── full pipeline ──────────────────────────────────────────────────────

    def run(self, record: MeetingRecord) -> dict:
        """End-to-end: persist → log → suggest cron → return result."""
        summary_path = self.persist_decision(record)
        self.log_execution(record, summary_path)
        cron_jobs = self.schedule_cron(record)

        return {
            "meeting_id": record.id,
            "verdict": record.final_verdict,
            "final_score": record.final_score,
            "summary_path": str(summary_path),
            "action_items": record.action_items,
            "suggested_cron": cron_jobs,
        }
