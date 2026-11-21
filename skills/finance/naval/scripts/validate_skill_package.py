#!/usr/bin/env python3
"""Minimal public package checks for NavalSKILL."""
from pathlib import Path
import re, sys, json

ROOT = Path(__file__).resolve().parents[1]
errors = []

skill = ROOT / "SKILL.md"
if not skill.exists():
    errors.append("SKILL.md missing")
else:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append("SKILL.md missing YAML frontmatter start")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append("SKILL.md frontmatter not closed")
    else:
        fm = m.group(1)
        if "name:" not in fm:
            errors.append("frontmatter missing name")
        if "description:" not in fm:
            errors.append("frontmatter missing description")
        # description char budget (frontmatter description block)
        desc = re.search(r"description:\s*\|?\s*\n((?:  .*\n)+)", fm)
        if desc and len(desc.group(1)) > 2000:
            errors.append("description block unusually long")
    for needle in ["Step 2.5", "🔴 CHECKPOINT", "🛑 STOP", "默认不超过 60"]:
        if needle not in text:
            errors.append(f"SKILL.md missing required marker: {needle}")
    if "/home/admin/" in text:
        errors.append("SKILL.md contains machine absolute path /home/admin/")

for req in ["README.md", "LICENSE", "test-prompts.json"]:
    if not (ROOT / req).exists():
        errors.append(f"missing {req}")

tp = ROOT / "test-prompts.json"
if tp.exists():
    try:
        data = json.loads(tp.read_text(encoding="utf-8"))
        if not isinstance(data, list) or len(data) < 3:
            errors.append("test-prompts.json should be a list with >=3 cases")
    except Exception as e:
        errors.append(f"test-prompts.json invalid: {e}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("PASS: package structure OK")
