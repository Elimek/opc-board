"""Generate dashboard for openrouter/owl-alpha board vote."""
import json
from pathlib import Path

data = json.load(open(r"C:\Users\Elimek\opc-board\memory\latest_board_vote.json", encoding="utf-8"))
votes = sorted(data["votes"], key=lambda v: v["score"])
out = Path(r"C:\Users\Elimek\opc-board\dashboard")

card_lines = []
for v in votes:
    s = v["score"]
    color = "#c0392b" if s < 4 else "#b8860b" if s < 6 else "#4e8c6e"
    rsn = v.get("reasoning", "")[:200]
    concerns_html = ""
    if v.get("key_concerns"):
        items = "".join(f'<div class="cn">\u00b7 {c}</div>' for c in v["key_concerns"][:2])
        concerns_html = f'<div class="cb"><b>Concerns ({len(v["key_concerns"])})</b>{items}</div>'
    card_lines.append(f'''
<div class="card">
  <div class="ch">
    <span>{v["agent_name"]}</span>
    <span class="rt">{v["role"]} &middot; {v["crew"]}</span>
    <span class="sc" style="color:{color}">{s}/10</span>
  </div>
  <div class="rsn">{rsn}</div>
  {concerns_html}
</div>''')

conds_lines = []
for v in votes:
    if v.get("conditions"):
        items = "".join(f"<li>{c}</li>" for c in v["conditions"][:3])
        conds_lines.append(f'<div class="cc"><b>{v["agent_name"]} ({v["role"]})</b><ul>{items}</ul></div>')

avg = data["average_score"]
total_c = sum(len(v.get("key_concerns",[])) for v in votes)
total_d = sum(len(v.get("conditions",[])) for v in votes)
hardest = min(votes, key=lambda x: x["score"])
softest = max(votes, key=lambda x: x["score"])

html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OPC Board — DCA 2026 Verdict (owl-alpha)</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Georgia,'Times New Roman',serif;background:#f0ece6;color:#2c2820;padding:2rem 1rem;font-size:15px;line-height:1.65}}
body::after{{content:'';position:fixed;inset:0;background-image:repeating-linear-gradient(0deg,transparent,transparent 28px,rgba(58,53,48,.08)28px,rgba(58,53,48,.08)29px);pointer-events:none;z-index:-1}}
h1{{text-align:center;font-size:1.9rem;font-weight:400;margin-bottom:.3rem}}
.subtitle{{text-align:center;color:#7a7268;font-style:italic;margin-bottom:.4rem}}
.meta{{text-align:center;color:#aaa;font-size:.72rem;font-family:Consolas,monospace;margin-bottom:1rem}}
.banner{{text-align:center;padding:.9rem 2rem;border-radius:5px;font-family:Helvetica,Arial,sans-serif;font-size:1rem;text-transform:uppercase;letter-spacing:.12em;margin:1rem auto;width:fit-content}}
.bf{{background:#fcecea;border:2px solid #c0392b;color:#c0392b}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:.9rem;margin:1.2rem 0}}
.card{{background:#fdfcf9;border:1px solid #e8e4dc;border-radius:5px;padding:1rem;box-shadow:1px 2px 8px rgba(0,0,0,.06)}}
.ch{{display:flex;align-items:center;gap:.5rem;margin-bottom:.4rem}}
.ch span{{font-weight:600;font-size:.88rem}}
.rt{{font-size:.68rem;text-transform:uppercase;letter-spacing:.07em;background:#e8e4dc;padding:1px 6px;border-radius:2px;color:#7a7268;margin-left:.5rem}}
.sc{{font-size:1.4rem;font-weight:bold;font-family:Helvetica,Arial,sans-serif;margin-left:auto}}
.rsn{{font-size:.8rem;color:#6a6258;font-style:italic;margin:.4rem 0;line-height:1.5}}
.cb{{margin-top:.4rem}}
.cb b{{font-family:Helvetica,Arial,sans-serif;font-size:.67rem;text-transform:uppercase;letter-spacing:.07em;color:#5a7a8a;display:block;margin-bottom:.1rem}}
.cn{{font-size:.74rem;color:#555;margin:.1rem 0 .1rem .8rem}}
.sm{{display:grid;grid-template-columns:auto auto;gap:.4rem 1.5rem;background:#fdfcf9;border:1px solid #e8e4dc;border-radius:5px;padding:.9rem 1.2rem;max-width:480px;margin:.8rem auto 1.4rem;font-size:.82rem}}
.sm b{{color:#2c2820}}.sm span{{color:#6a6258}}
.sec{{font-family:Helvetica,Arial,sans-serif;font-size:.82rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;margin:1.8rem 0 .7rem;padding-bottom:.3rem;border-bottom:1.5px solid #e8e4dc}}
.cg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:.8rem;margin:.5rem 0}}
.cc{{background:#fdfcf9;border:1px dashed #d0c9be;border-radius:4px;padding:.7rem .9rem;font-size:.76rem}}
.cc b{{display:block;margin-bottom:.2rem;font-size:.78rem;font-family:Helvetica,Arial,sans-serif}}
.cc li{{margin:.12rem 0;color:#4a4a4a}}
.footer{{text-align:right;font-size:.7rem;color:#bbb;font-style:italic;margin-top:2rem}}
</style>
</head>
<body>
<h1>OPC Board &middot; DCA 2026 Verdict</h1>
<p class="subtitle">50% QQQM &middot; 25% SOXQ &middot; 25% TQQQ &middot; $1,000/mo &middot; July 2026</p>
<p class="meta">Model: openrouter/owl-alpha &middot; 10/10 live LLM votes &middot; {data['timestamp']} &middot; Wall {data['wall_time_sec']}s</p>
<div class="banner bf">\u274c Group Verdict: FAIL &middot; {data['average_score']}/10</div>
<div class="sm">
  <b>Model:</b><span>openrouter/owl-alpha (OpenRouter)</span>
  <b>Avg:</b><span>{avg}/10</span>
  <b>Verdict:</b><span>FAIL</span>
  <b>Consensus:</b><span>TQQQ 3x leverage rejected by all 10</span>
  <b>Concerns total:</b><span>{total_c}</span>
  <b>Conditions total:</b><span>{total_d}</span>
  <b>Wall time:</b><span>{data['wall_time_sec']}s / ~{data.get("votes",[{}])[0].get("agent_name","")}min serial</span>
  <b>Hardest:</b><span>{hardest['agent_name']} {hardest['score']}/10</span>
  <b>Softest:</b><span>{softest['agent_name']} {softest['score']}/10</span>
</div>
<div class="sec">10 Agent Scorecards</div>
<div class="grid">
{chr(10).join(card_lines)}
</div>
<div class="sec">Conditions to Reach Score &ge; 6</div>
<div class="cg">
{chr(10).join(conds_lines)}
</div>
<div class="footer">OPC Board &middot; Hermes Agent + OpenRouter owl-alpha &middot; memory/latest_board_vote.json</div>
</body>
</html>"""

(out / "dca-2026-verdict-owalpha.html").write_text(html, encoding="utf-8")
print(f"Written -> dashboard/dca-2026-verdict-owalpha.html")
