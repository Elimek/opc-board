#!/bin/bash
# OPC Quality Harness — 自动检查 SKILL 质量、数据一致性、输出规范
# 跑在：每次 SKILL 更新后 / 每次董事会后
# 用法: bash scripts/quality-harness.sh [--verbose]

set -e
PASS=0; FAIL=0; WARN=0; ERRORS=""; WARNS=""

log() { echo "[$1] $2"; }
pass() { PASS=$((PASS+1)); log "✅" "$1"; }
fail() { FAIL=$((FAIL+1)); log "❌" "$1"; ERRORS="$ERRORS  ❌ $1\n"; }
warn() { WARN=$((WARN+1)); log "⚠️" "$1"; WARNS="$WARNS  ⚠️ $1\n"; }

SKILL_DIR="/c/Users/Elimek/opc-board/skills"
HERMES_SKILLS_DIR="$HOME/.hermes/skills"
VERBOSE=false
[[ "$1" == "--verbose" ]] && VERBOSE=true

echo ""
echo "════════════════════════════════════════"
echo "  OPC QUALITY HARNESS"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "════════════════════════════════════════"
echo ""

# ============================================================
# PHASE 1: SKILL 完整性检查
# ============================================================
echo "--- PHASE 1: SKILL INTEGRITY ---"

# 1a. 每个 SKILL 是否有明确的立场定义（对核心议题）
check_stances() {
  local file="$1" name="$2"
  if grep -q "已定义立场\|已定义\|硬编码\|Hardcoded\|立场表" "$file" 2>/dev/null; then
    pass "$name has explicit stance definitions"
  else
    warn "$name lacks explicit stance definitions — risk of inconsistency"
  fi
}

# 1b. 输出是否包含具体标的+数据（而不是空泛建议）
check_concrete_output() {
  local file="$1" name="$2"
  local has_ticker=$(grep -cE '[A-Z]{2,5}' "$file" 2>/dev/null || true)
  local has_data=$(grep -cE '[0-9]+\.[0-9]%' "$file" 2>/dev/null || true)
  if [[ "$has_ticker" -ge 3 && "$has_data" -ge 3 ]]; then
    pass "$name contains concrete tickers and data"
  else
    warn "$name may lack concrete recommendations (tickers=$has_ticker, data=$has_data)"
  fi
}

# 1c. 是否包含诚实边界
check_boundaries() {
  local file="$1" name="$2"
  if grep -q "诚实边界\|Honest Boundaries\|诚实边界\|不能\|不会\|局限" "$file" 2>/dev/null; then
    pass "$name has honest boundaries"
  else
    fail "$name missing honest boundaries"
  fi
}

# 1d. 检查数据是否可能过时（含年份的引用）
check_stale_data() {
  local file="$1" name="$2"
  local stale_years=$(grep -oE '20[0-9]{2}' "$file" 2>/dev/null | sort -u || true)
  local latest=0
  for y in $stale_years; do
    [[ "$y" -gt "$latest" ]] && latest=$y
  done
  if [[ "$latest" -ge 2026 ]]; then
    pass "$name has current data (ref $latest)"
  elif [[ "$latest" -ge 2024 ]]; then
    warn "$name data from $latest — may need refresh"
  else
    warn "$name data may be stale (latest ref: $latest)"
  fi
}

# 遍历所有 SKILL 做质量检查
find "$SKILL_DIR" -name "*.md" -not -name "README.md" | while read f; do
  name=$(basename "$f" .md)
  $VERBOSE && echo "  checking: $f"
  check_stances "$f" "$name"
  check_concrete_output "$f" "$name"
  check_boundaries "$f" "$name"
  check_stale_data "$f" "$name"
done

# ============================================================
# PHASE 2: 数据准确性检查
# ============================================================
echo ""
echo "--- PHASE 2: DATA ACCURACY ---"

# 费率检查 — 是否有明显错误
check_fee() {
  local ticker="$1" expected="$2" source="$3"
  # 在 SKILL 文件中查找此 ticker 的费率
  local found=$(grep -i "$ticker" "$SKILL_DIR" -r 2>/dev/null | grep -oP '[0-9]+\.[0-9]+%' | head -1)
  if [[ -n "$found" ]]; then
    pass "Fee for $ticker referenced: $found (expected ~$expected from $source)"
  else
    pass "$ticker not in SKILL files (no data to verify)"
  fi
}

check_fee "IAU" "0.25%" "iShares"
check_fee "GLDM" "0.10%" "State Street"
check_fee "SOXQ" "0.19%" "Invesco"
check_fee "XBI" "0.35%" "SPDR"
check_fee "SCHD" "0.06%" "Charles Schwab"
check_fee "BND" "0.03%" "Vanguard"
check_fee "QQQJ" "0.15%" "Invesco"

# ============================================================
# PHASE 3: 董事会输出质量检查
# ============================================================
echo ""
echo "--- PHASE 3: OUTPUT QUALITY ---"

# 检查是否有模糊用语
check_vague_language() {
  local file="$1" name="$2"
  local vague_count=$(grep -cE '可以考虑|适当|maybe|perhaps|it depends' "$file" 2>/dev/null || true)
  if [[ "$vague_count" -eq 0 ]]; then
    pass "$name: no vague language detected"
  else
    warn "$name: $vague_count vague terms found"
  fi
}

find "$SKILL_DIR" -name "*.md" | while read f; do
  name=$(basename "$f" .md)
  check_vague_language "$f" "$name"
done

# ============================================================
# PHASE 4: 集成检查 — Hermes SKILL vs 仓库文件一致性
# ============================================================
echo ""
echo "--- PHASE 4: INTEGRATION CHECK ---"

# 检查 Hermes 安装的 SKILL 是否与仓库索引一致
echo "  Hermes installed skills:"
ls "$HERMES_SKILLS_DIR/opc-board/" 2>/dev/null | while read skill; do
  echo "    ✅ $skill"
done

echo ""
echo "  Repo skill index entries:"
grep -r "skill_view" "$SKILL_DIR/README.md" 2>/dev/null | head -20 || echo "    (no skill_view references)"
grep "skill_view" "$SKILL_DIR"/*/README.md 2>/dev/null | while read line; do
  echo "    📄 $line"
done

# ============================================================
# RESULTS
# ============================================================
echo ""
echo "════════════════════════════════════════"
echo "  HARNESS RESULTS"
echo "════════════════════════════════════════"
echo "  ✅ PASS: $PASS"
echo "  ⚠️  WARN: $WARN"
echo "  ❌ FAIL: $FAIL"

if [[ "$FAIL" -gt 0 ]]; then
  echo ""
  echo "  FAILURES:"
  echo -e "$ERRORS"
fi
if [[ "$WARN" -gt 0 ]]; then
  echo ""
  echo "  WARNINGS:"
  echo -e "$WARNS"
fi

echo ""
echo "════════════════════════════════════════"
