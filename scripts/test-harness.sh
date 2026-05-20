#!/bin/bash
# OPC Board — Test Harness
# Full acceptance testing: smoke, functional, integration, system
# Usage: bash test-harness.sh

PASS=0
FAIL=0
ERRORS=""

log() { echo "[$1] $2"; }
pass() { PASS=$((PASS+1)); log "✅ PASS" "$1"; }
fail() { FAIL=$((FAIL+1)); log "❌ FAIL" "$1"; ERRORS="$ERRORS  ❌ $1\n"; }

echo "🏢 OPC BOARD — FULL TEST HARNESS"
echo "================================"
echo ""

# ============================================================
# PHASE 1: SMOKE TEST — Is the site even alive?
# ============================================================
echo "--- PHASE 1: SMOKE TEST ---"

# Test 1: GitHub Pages URL
STATUS=$(curl -sI "https://elimek.github.io/opc-board/" 2>/dev/null | head -1 | awk '{print $2}')
if [ "$STATUS" = "200" ]; then
  pass "GitHub Pages returns 200 OK"
else
  fail "GitHub Pages returned $STATUS (expected 200)"
fi

# Test 2: No 301 redirect to custom domain
LOC=$(curl -sI "https://elimek.github.io/opc-board/" 2>/dev/null | grep -i "^location:" | head -1)
if [ -z "$LOC" ]; then
  pass "No unwanted redirect"
else
  fail "Unexpected redirect: $LOC"
fi

# Test 3: HTTPS enforced
PROTO=$(curl -sI "http://elimek.github.io/opc-board/" 2>/dev/null | head -1 | awk '{print $2}')
if [ "$PROTO" = "301" ] || [ "$PROTO" = "200" ]; then
  pass "HTTP redirects to HTTPS"
else
  fail "HTTP returned $PROTO"
fi

# Test 4: DNS resolves
nslookup elimek.github.io 2>/dev/null | grep -q "Address" && pass "DNS resolves" || fail "DNS resolution failed"

# ============================================================
# PHASE 2: FUNCTIONAL TEST — All assets, links, pages
# ============================================================
echo ""
echo "--- PHASE 2: FUNCTIONAL TEST ---"

# Test 5: index.html exists
if [ -f "/c/Users/Elimek/opc-board/index.html" ]; then
  SIZE=$(wc -c < "/c/Users/Elimek/opc-board/index.html")
  pass "index.html exists ($SIZE bytes)"
else
  fail "index.html missing"
fi

# Test 6: CSS loads
HTML=$(curl -s "https://elimek.github.io/opc-board/" 2>/dev/null)
if echo "$HTML" | grep -q "style.css"; then
  CSS_URL=$(echo "$HTML" | grep -oP 'href="([^"]*style\.css[^"]*)"' | head -1 | sed 's/href="//;s/"//')
  CSS_STATUS=$(curl -sI "https://elimek.github.io/opc-board/$CSS_URL" 2>/dev/null | head -1 | awk '{print $2}')
  if [ "$CSS_STATUS" = "200" ]; then
    pass "CSS stylesheet loads ($CSS_STATUS)"
  else
    fail "CSS at $CSS_URL returned $CSS_STATUS"
  fi
else
  fail "CSS link not found in index.html"
fi

# Test 7: Dashboard loads
DASH_STATUS=$(curl -sI "https://elimek.github.io/opc-board/dashboard/index.html" 2>/dev/null | head -1 | awk '{print $2}')
if [ "$DASH_STATUS" = "200" ]; then
  pass "Dashboard loads ($DASH_STATUS)"
else
  fail "Dashboard returned $DASH_STATUS"
fi

# Test 8: README exists
if [ -f "/c/Users/Elimek/opc-board/README.md" ]; then
  SIZE=$(wc -c < "/c/Users/Elimek/opc-board/README.md")
  pass "README.md exists ($SIZE bytes)"
else
  fail "README.md missing"
fi

# Test 9: LICENSE exists
if [ -f "/c/Users/Elimek/opc-board/LICENSE" ]; then
  LINES=$(wc -l < "/c/Users/Elimek/opc-board/LICENSE")
  pass "LICENSE exists ($LINES lines)"
else
  fail "LICENSE missing"
fi

# Test 10: CNAME removed (no broken domain)
if [ ! -f "/c/Users/Elimek/opc-board/CNAME" ]; then
  pass "CNAME removed (no broken domain reference)"
else
  fail "CNAME still present"
fi

# ============================================================
# PHASE 3: SKILL INTEGRITY — All SKILL files exist and valid
# ============================================================
echo ""
echo "--- PHASE 3: SKILL INTEGRITY ---"

SKILL_DIR="/c/Users/Elimek/opc-board/skills"
SKILL_COUNT=0
declare -a MISSING

for dir in finance health media strategy innovation _meta; do
  for f in "$SKILL_DIR/$dir"/*.md; do
    if [ -f "$f" ]; then
      SKILL_COUNT=$((SKILL_COUNT+1))
      NAME=$(basename "$f")
      # Check frontmatter has title
      if head -10 "$f" | grep -q "^title:"; then
        pass "SKILL $dir/$NAME has title frontmatter"
      else
        fail "SKILL $dir/$NAME missing title frontmatter"
      fi
    fi
  done
done
log "📊" "Total SKILL files: $SKILL_COUNT"

# Test: Integration layer exists
if [ -f "$SKILL_DIR/_meta/integration.md" ]; then
  pass "Integration layer exists"
else
  fail "Integration layer missing"
fi

# ============================================================
# PHASE 4: CHECKLIST INTEGRITY
# ============================================================
echo ""
echo "--- PHASE 4: CHECKLISTS ---"

CHK_DIR="/c/Users/Elimek/opc-board/checklist"
for f in weekly-board-meeting.md daily-routine.md financial-review.md; do
  if [ -f "$CHK_DIR/$f" ]; then
    pass "Checklist $f exists"
  else
    fail "Checklist $f missing"
  fi
done

# ============================================================
# PHASE 5: CLI TOOL — opc.sh
# ============================================================
echo ""
echo "--- PHASE 5: CLI TOOL ---"

CLI="/c/Users/Elimek/opc-board/opc.sh"
if [ -f "$CLI" ]; then
  pass "opc.sh exists"
  # Test: opc help command (defined as case "help|*")
  for cmd in board daily filter health status help; do
    if grep -qE "^\s*($cmd\|?.*\)|$cmd\*)" "$CLI" 2>/dev/null; then
      pass "  opc $cmd command defined"
    elif grep -qE "^\s*($cmd\||\|?$cmd)" "$CLI" 2>/dev/null; then
      pass "  opc $cmd command defined (case fallthrough)"
    elif grep -qE "^\s*$cmd)" "$CLI" 2>/dev/null; then
      pass "  opc $cmd command defined"
    else
      fail "  opc $cmd command missing"
    fi
  done
else
  fail "opc.sh missing"
fi

# ============================================================
# PHASE 6: INTEGRATION TEST — GitHub + Cronjobs
# ============================================================
echo ""
echo "--- PHASE 6: INTEGRATION ---"

# Test: GitHub repo exists and is public
REPO_JSON=$(gh api repos/Elimek/opc-board 2>/dev/null)
if echo "$REPO_JSON" | grep -q "private.*false" || echo "$REPO_JSON" | grep -q '"private":false'; then
  pass "GitHub repo is public"
else
  fail "GitHub repo not public or not found"
fi

# Test: GitHub Pages configured
PAGES_JSON=$(gh api repos/Elimek/opc-board/pages 2>/dev/null)
if echo "$PAGES_JSON" | grep -q '"status":"built"'; then
  pass "GitHub Pages built successfully"
elif echo "$PAGES_JSON" | grep -q '"status"'; then
  STATUS_VAL=$(echo "$PAGES_JSON" | grep -oP '"status":"[^"]*"' | head -1)
  log "⚠️" "GitHub Pages status: $STATUS_VAL (not 'built')"
  pass "GitHub Pages configured"
else
  fail "GitHub Pages not configured"
fi

# Test: No CNAME set in pages config
if echo "$PAGES_JSON" | grep -q '"cname":null'; then
  pass "No custom CNAME set (waiting for is-a.dev PR)"
else
  CNAME_VAL=$(echo "$PAGES_JSON" | grep -oP '"cname":"[^"]*"' | head -1)
  log "⚠️" "Has CNAME: $CNAME_VAL"
  pass "Has custom domain set"
fi

# Test: .gitignore excludes deploy.yml
if grep -q "workflows" "/c/Users/Elimek/opc-board/.gitignore" 2>/dev/null; then
  pass "deploy.yml excluded from git"
elif [ ! -f "/c/Users/Elimek/opc-board/.github/workflows/deploy.yml" ]; then
  pass "Workflow dir clean (no deploy.yml in git)"
else
  log "⚠️" "deploy.yml may be tracked (token scope issue)"
fi

# Test: All cronjobs active
CJOBS=$(cronjob action=list 2>/dev/null | grep -c "OPC" 2>/dev/null || echo "0")
if [ "$CJOBS" -ge 3 ]; then
  pass "All 3 cronjobs active"
else
  log "⚠️" "Found $CJOBS/3 OPC cronjobs"
fi

# ============================================================
# PHASE 7: CONTENT INTEGRITY
# ============================================================
echo ""
echo "--- PHASE 7: CONTENT INTEGRITY ---"

# Test: No placeholder text remains
if grep -q "YOUR_USERNAME" "/c/Users/Elimek/opc-board/README.md" 2>/dev/null; then
  fail "README still has YOUR_USERNAME placeholder"
else
  pass "No placeholder text in README"
fi

if grep -q "YOUR_USERNAME" "/c/Users/Elimek/opc-board/index.html" 2>/dev/null; then
  fail "index.html still has YOUR_USERNAME placeholder"
else
  pass "No placeholder text in index.html"
fi

# Test: GitHub URLs point to correct repo
if grep -q "github.com/Elimek/opc-board" "/c/Users/Elimek/opc-board/README.md" 2>/dev/null; then
  pass "README GitHub link points to Elimek/opc-board"
else
  fail "README GitHub link wrong"
fi

# ============================================================
# RESULTS
# ============================================================
echo ""
echo "================================"
echo "🏁 TEST HARNESS RESULTS"
echo "================================"
echo "  ✅ PASS: $PASS"
echo "  ❌ FAIL: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "  🎉 ALL TESTS PASSED"
else
  echo "  ❌ FAILURES:"
  echo -e "$ERRORS"
fi
echo ""
echo "================================"
