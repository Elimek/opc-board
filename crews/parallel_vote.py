"""Parallel 10-agent board meeting — Topic: July 2026 DCA ($1000/mo, QQQM+SOXQ+TQQQ)"""
import subprocess, time, json, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, r"C:\Users\Elimek\opc-board")
from crews.coordinator import BoardCoordinator, _strip_session_id, _parse_vote_json
from crews.registry_loader import load_registry

TOPIC = "July 2026 DCA board review: $1000/mo. 50% QQQM | 25% SOXQ | 25% TQQQ"
CONTEXT = {
    "monthly_amount": 1000,
    "salary": 4000,
    "risk_tolerance": "50%_max_drawdown",
    "user_skill": "zero_finance_experience",
    "start_date": "July 2026",
}

reg = load_registry()
coord = BoardCoordinator()
coord._topic = TOPIC
coord._context = CONTEXT


def _call_one(agent):
    prompt = coord._build_agent_prompt(agent, round_num=1)
    t0 = time.time()
    proc = subprocess.run(
        ["hermes", "chat", "-q", prompt, "-Q"],
        capture_output=True, text=True, timeout=75,
    )
    raw = _strip_session_id(proc.stdout.strip()) if proc.returncode == 0 else ""
    dt = time.time() - t0
    parsed = _parse_vote_json(raw)
    return {
        "agent_id": agent["id"],
        "agent_name": agent["name"],
        "role": agent["role"],
        "crew": agent["crew"],
        "score": parsed.get("score", 5),
        "reasoning": parsed.get("reasoning", ""),
        "key_concerns": parsed.get("key_concerns", []),
        "conditions": parsed.get("conditions", []),
        "elapsed": round(dt, 1),
        "raw_snippet": raw[:120],
    }


if __name__ == "__main__":
    results = []
    t0_all = time.time()
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(_call_one, a): a for a in reg["agents"]}
        for f in as_completed(futures):
            r = f.result()
            results.append(r)
    wall_time = time.time() - t0_all

    results.sort(key=lambda x: x["agent_id"])

    print(f"\n{'='*60}")
    print(f"  BOARD VOTE: {TOPIC}")
    print(f"{'='*60}")
    print(f"  {'Agent':22s} {'Role':5s} Score  Time  Summary")
    print(f"  {'-'*52}")

    for r in results:
        style = "GREEN" if r["score"] >= 6 else "RED"
        stars = "*" * r["score"] + "." * (10 - r["score"])
        print(f"  [{style}] {r['agent_name']:22s} {r['role']:5s} {r['score']}/10  "
              f"({r['elapsed']}s)  {r['reasoning'][:65]}[{style}]")

    scores = [r["score"] for r in results]
    avg = sum(scores) / len(scores)
    verdict = "PASS" if avg >= 6 else "FAIL"
    print(f"\n  {'='*50}")
    print(f"  Avg score : {avg:.2f}/10")
    print(f"  Min / Max : {min(scores)} / {max(scores)}")
    print(f"  Verdict   : {verdict.upper()}")
    print(f"  Wall time : {wall_time:.1f}s  "
          f"(serial seriaison ~{sum(r['elapsed'] for r in results):.0f}s saved)")
    print(f"{'='*50}")

    # Save JSON
    out = {
        "topic": TOPIC,
        "context": CONTEXT,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "wall_time_sec": round(wall_time, 1),
        "average_score": round(avg, 2),
        "verdict": verdict,
        "votes": results,
    }
    with open(r"C:\Users\Elimek\opc-board\memory\latest_board_vote.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("\n  Saved: memory/latest_board_vote.json")
