"""Parallel 10-agent board — live openrouter/owl-alpha"""
import subprocess, sys, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, r"C:\Users\Elimek\opc-board")
from crews.registry_loader import load_registry
from crews.coordinator import _call_agent, _parse_vote_json

# ── board coordinator helper ───────────────────────────────────
def build_prompt(agent, topic, ctx, round_num, dissent=""):
    ctx_str = json.dumps(ctx, ensure_ascii=False) if ctx else ""
    base = (
        f"## Role: {agent['name']} | {agent['role']}\n"
        f"{agent['system_prompt']}\n"
        f"## Decision for CEO\n"
        f"Topic: {topic}\n"
        + (f"Context/Data provided by CEO:\n{ctx_str}\n" if ctx else "\n")
        + ("This is the FIRST round. Do not hold back.\n" if round_num == 1
           else f"Re-examine comments from peers below:\n{dissent}\n")
    )
    base += (
        "\n---\n"
        "Output **strict JSON** (no markdown, no extra text):\n"
        '{"score": <1-10 int>, "reasoning": "<3-5 sentences>", '
        '"key_concerns": ["..."], "conditions": ["<what must be true for you to raise your score>"], '
        '"reason_changed": "<why this round differs, or blank if same>"}'
    )
    return base

reg = load_registry()
agents = reg["agents"]
TOPIC = "July 2026 DCA: $1,000/month. 50% QQQM | 25% SOXQ | 25% TQQQ"
CTX = dict(monthly_amount=1000, salary=4000, risk_tolerance="max50%_drawdown", user_skill="zero_finance_experience", start_date="July 2026")
N = len(agents)

print(f"10-agent board · {N} directors · openrouter/owl-alpha\n")

def do_vote(agent):
    prompt = build_prompt(agent, TOPIC, CTX, 1)
    raw = _call_agent(agent, prompt)
    parsed = _parse_vote_json(raw)
    return dict(
        agent_id=agent["id"], agent_name=agent["name"], role=agent["role"],
        crew=agent["crew"], score=parsed.get("score", 5),
        reasoning=parsed.get("reasoning", ""),
        key_concerns=parsed.get("key_concerns", []),
        conditions=parsed.get("conditions", []),
        raw_snippet=raw[:500],
    ), raw

t0 = time.time()
votes = []
with ThreadPoolExecutor(max_workers=10) as pool:
    fmap = {pool.submit(do_vote, a): a for a in agents}
    for f in as_completed(fmap):
        a = fmap[f]
        try:
            v, raw = f.result()
            votes.append(v)
            bar = "█" * v["score"] + "░" * (10 - v["score"])
            print(f"  [{v['score']}] {bar} {v['agent_name']:22s} ({v['role']})  {time.time()-t0:.0f}s")
        except Exception as e:
            print(f"  ✗ {a['name']:22s} ERROR: {e}")
            votes.append(dict(agent_id=a["id"], agent_name=a["name"], role=a["role"],
                              crew=a["crew"], score=5, reasoning=str(e),
                              key_concerns=[], conditions=[], raw_snippet=""))

elapsed = time.time() - t0
votes.sort(key=lambda v: v["score"])
avg = sum(v["score"] for v in votes) / len(votes)

print(f"\n{'='*60}")
print(f"  Average: {avg:.1f}/10  Verdict: {'PASS ✅' if avg >= 6 else 'FAIL ❌'}")
print(f"  Wall time: {elapsed:.0f}s  (serial equivalent ~{N*35:.0f}s · saved {N*35 - elapsed:.0f}s)")

# ── Save ─────────────────────────────────────────────────────
summary = {"topic": TOPIC, "context": CTX, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
           "wall_time_sec": round(elapsed), "average_score": round(avg, 1),
           "verdict": "PASS" if avg >= 6 else "FAIL", "votes": votes}
out_path = Path(r"C:\Users\Elimek\opc-board\memory\latest_board_vote.json")
out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nSaved → {out_path}")
print(f"\nTop gospel: {max(votes, key=lambda v: v['score'])['agent_name']} ({max(v for v in votes if v['score']==0)})")
