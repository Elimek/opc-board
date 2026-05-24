#!/bin/bash
# OPC Board — CLI Tool v2
# Usage: bash opc.sh [command]
# Commands: board, daily, filter, health, status, agents, history, help

set -e

OPC_DIR="$(cd "$(dirname "$0")" && pwd)"

case "${1:-help}" in
  board)
    # Delegate to Python crews-based board meeting if available
    if [ -f "$OPC_DIR/opc.py" ]; then
      exec python "$OPC_DIR/opc.py" board "${@:2}"
    fi
    # Fallback: simple prompt-based deliberation
    shift
    TOPIC="${1:-$(read -p "What's your current challenge or decision? " ans; echo "$ans")}"
    echo ""
    echo "--- Meeting called to order ---"
    echo "Agenda: $TOPIC"
    echo ""
    echo "💼  FINANCE CEO (Naval / Buffett / Duan / Trump)"
    echo "  - Can you productize this? (zero marginal cost?)"
    echo "  - What's the moat? Will it compound over 10 years?"
    echo "  - Cash flow: does this pay you now or later?"
    echo "  - Would Duan Yongping say '我懂这个'?"
    echo ""
    echo "🧬  HEALTH CEO (Bryan Johnson / Huberman)"
    echo "  - Will this decision improve or harm your sleep?"
    echo "  - What's the stress cost? Can you sustain it?"
    echo "  - Are you optimizing the right thing?"
    echo "  - Bryan Johnson: is this 'Don't Die' compliant?"
    echo ""
    echo "📱  MEDIA CEO (Dan Koe)"
    echo "  - Can you document this journey publicly?"
    echo "  - What content can you create from this?"
    echo "  - Who is 6 months behind you on this path?"
    echo "  - What's the product hook?"
    echo ""
    echo "🧠  STRATEGY (Zhang Xuedong / Lidangzzz)"
    echo "  - ROI for an ordinary person?"
    echo "  - Data or emotion driving this decision?"
    echo "  - What's the worst case? Can you survive it?"
    echo "  - Lidangzzz: is this a trap?"
    echo ""
    echo "🚀  INNOVATION CEO (Elon Musk)"
    echo "  - First principles: what's the fundamental truth here?"
    echo "  - Can you delete 50% of what you're planning?"
    echo "  - What's the 2-week MVP?"
    echo "  - What would an unreasonable person try?"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  For AI-powered board voting: bash opc.sh agents"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ;;

  agents)
    if [ -f "$OPC_DIR/opc.py" ]; then
      exec python "$OPC_DIR/opc.py" agents
    fi
    echo "🏢  10 BOARD MEMBERS"
    echo "  Finance:  Naval, Buffett, Duan Yongping"
    echo "  Brand:    Trump, Dan Koe"
    echo "  Health:   Bryan Johnson, Huberman"
    echo "  Strategy: Zhang Xuedong, Lidangzzz"
    echo "  Innovation: Elon Musk"
    ;;

  history)
    if [ -f "$OPC_DIR/opc.py" ]; then
      exec python "$OPC_DIR/opc.py" history "${@:2}"
    fi
    echo "📋  Meeting history not available in fallback mode."
    ;;

  daily)
    echo "🌅  DAILY OS"
    echo "============"
    echo ""
    echo "Date: $(date +%Y-%m-%d)"
    echo ""
    echo "  MORNING"
    echo "  ☀️  Sunlight 10min"
    echo "  🚫  No caffeine 90min"
    echo "  🧠  Deep work #1: 90min"
    echo ""
    echo "  MIDDAY"
    echo "  🥗  Whole food lunch"
    echo "  🚶  Walk 20min"
    echo ""
    echo "  AFTERNOON"
    echo "  🏋️  Exercise (strength 3×, cardio 2×, mobility daily)"
    echo "  🧠  Deep work #2: 90min"
    echo ""
    echo "  EVENING"
    echo "  🥘  Light dinner (3h before bed)"
    echo "  📵  No screens 1h before bed"
    echo "  📓  Journal & plan tomorrow"
    echo ""
    echo "  NIGHT"
    echo "  😴  8+ hours sleep"
    ;;
  filter)
    shift
    if [ $# -eq 0 ]; then
      echo "Usage: opc filter \"your question\""
      exit 1
    fi
    QUESTION="$*"
    echo "🔍  5-FILTER DECISION"
    echo "====================="
    echo "Question: $QUESTION"
    echo ""
    echo "1️⃣  STRATEGY — ROI? $_$(echo "$QUESTION" | grep -qiE '(cost|pay|money|rent|fuel)' && echo '⚠ Check numbers' || echo '✓ No money signal')"
    echo "2️⃣  FINANCE — Compounds? $_$(echo "$QUESTION" | grep -qiE '(build|create|learn|skill|ship)' && echo '✓ Building = compounds' || echo '⚠ Not compound-positive')"
    echo "3️⃣  HEALTH — Harmless? $_$(echo "$QUESTION" | grep -qiE '(sleep|stress|burn|exhaust|16h)' && echo '⚠ Health risk' || echo '✓ No health flags')"
    echo "4️⃣  MEDIA — Can you create content? $_$(echo "$QUESTION" | grep -qiE '(teach|share|show|tweet|write)' && echo '✓ Content angle' || echo '— No content signal')"
    echo "5️⃣  INNOVATION — Better way?  [assume YES — always question assumptions]"
    echo ""
    echo "→ 3+ YES = proceed | 3+ NO = stop"
    ;;
  health)
    echo "🧬  HEALTH TRACKER"
    echo "=================="
    echo "Date: $(date +%Y-%m-%d)"
    echo ""
    echo "  AM CHECK"
    echo "  ☑  Sunlight before 9am"
    echo "  ☑  No caffeine 90min"
    echo "  ☑  500ml water"
    echo ""
    echo "  NUTRITION"
    echo "  ☑  High-protein breakfast"
    echo "  ☑  Lunch: whole food + protein"
    echo "  ☑  Dinner: 3h before bed"
    echo ""
    echo "  MOVEMENT"
    echo "  ☑  Strength (___ min)"
    echo "  ☑  Cardio / walk (___ min)"
    echo "  ☑  Stretch"
    echo ""
    echo "  SLEEP"
    echo "  ☑  Same bedtime"
    echo "  ☑  No screens 1h before"
    echo "  ☑  Room dark + cool"
    ;;
  status)
    echo "📊  OPC STATUS"
    echo "=============="
    echo ""
    echo "  🏛️  Board: READY"
    echo "  💼  Finance: 3 SKILLs loaded"
    echo "  🧬  Health: 2 SKILLs loaded"
    echo "  📱  Media: 1 SKILL loaded"
    echo "  🧠  Strategy: 2 SKILLs loaded"
    echo "  🚀  Innovation: 1 SKILL loaded"
    echo ""
    echo "  🌐  GitHub: https://github.com/Elimek/opc-board"
    if [ -f "$OPC_DIR/meetings/meetings.jsonl" ]; then
      echo "  📋  Meetings on record: $(wc -l < "$OPC_DIR/meetings/meetings.jsonl")"
    fi
    if [ -f "$OPC_DIR/opc.py" ]; then
      echo "  ⚡  Crew mode: ACTIVE (python opc.py)"
    else
      echo "  ⚠️  Crew mode: fallback-shell only"
      echo "       Install Python deps: pip install typer rich pyyaml"
    fi
    ;;
  help|*)
    echo "🏢  OPC BOARD — One-Person Company CLI v2"
    echo ""
    echo "Commands:"
    echo "  opc board        Start a board meeting (AI crew voting)"
    echo "  opc board \"topic\"  Start meeting with explicit topic"
    echo "  opc agents       List all 10 board members"
    echo "  opc history      Show recent meetings"
    echo "  opc daily        Show daily OS routine"
    echo "  opc filter \"q\"  Run 5-filter protocol"
    echo "  opc health       Health tracker"
    echo "  opc status       System status"
    echo "  opc help         Show this"
    echo ""
    echo "Usage:"
    echo "  bash opc.sh board \"Should I DCA QQQM + SOXQ + TQQQ in July?\""
    ;;
esac
