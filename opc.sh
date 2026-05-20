#!/bin/bash
# OPC Board — CLI Tool
# One-Person Company Operating System
# Usage: bash opc.sh [command]
# Commands: board, daily, filter, health, status, help

set -e

OPC_DIR="$(cd "$(dirname "$0")" && pwd)"

case "${1:-help}" in
  board)
    echo "🏛️  OPC BOARD MEETING"
    echo "===================="
    echo ""
    echo "What's your current challenge or decision?"
    read -r CHALLENGE
    echo ""
    echo "--- Meeting called to order ---"
    echo "Agenda: $CHALLENGE"
    echo ""

    # Finance CEO
    echo "💼  FINANCE CEO (Naval / Buffett / Duan / Trump)"
    echo "  - Can you productize this? (zero marginal cost?)"
    echo "  - What's the moat? Will it compound over 10 years?"
    echo "  - Cash flow: does this pay you now or later?"
    echo "  - Would Duan Yongping say '我懂这个'?"
    echo ""

    # Health CEO
    echo "🧬  HEALTH CEO (Bryan Johnson / Huberman)"
    echo "  - Will this decision improve or harm your sleep?"
    echo "  - What's the stress cost? Can you sustain it?"
    echo "  - Are you optimizing the right thing?"
    echo "  - Bryan Johnson: is this 'Don't Die' compliant?"
    echo ""

    # Media CEO
    echo "📱  MEDIA CEO (Dan Koe)"
    echo "  - Can you document this journey publicly?"
    echo "  - What content can you create from this?"
    echo "  - Who is 6 months behind you on this path?"
    echo "  - What's the product hook?"
    echo ""

    # Strategy
    echo "🧠  STRATEGY (Zhang Xuedong / Lidangzzz)"
    echo "  - ROI for an ordinary person?"
    echo "  - Data or emotion driving this decision?"
    echo "  - What's the worst case? Can you survive it?"
    echo "  - Lidangzzz: is this a trap?"
    echo ""

    # Innovation
    echo "🚀  INNOVATION CEO (Elon Musk)"
    echo "  - First principles: what's the fundamental truth here?"
    echo "  - Can you delete 50% of what you're planning?"
    echo "  - What's the 2-week MVP?"
    echo "  - What would an unreasonable person try?"
    echo ""

    echo "--- Meeting adjourned ---"
    echo ""
    echo "Your action items:"
    echo "  1. One thing to START:"
    echo "  2. One thing to STOP:"
    echo "  3. One thing to CONTINUE:"
    ;;

  daily)
    echo "🌅  DAILY OS"
    echo "============"
    echo ""
    echo "  MORNING (6:00-8:00)"
    echo "  ☀️  Sunlight 10min"
    echo "  🚫  No caffeine for 90min"
    echo "  ❄️  Cold shower (optional)"
    echo "  🧠  Deep work block #1 (90min)"
    echo ""
    echo "  MIDDAY (12:00-14:00)"
    echo "  🥗  Whole food lunch"
    echo "  🚶  Walk 10-20min"
    echo "  💤  NSDR or nap 10-20min"
    echo ""
    echo "  AFTERNOON (14:00-18:00)"
    echo "  🏋️  Exercise (strength 3x, cardio 2x, mobility daily)"
    echo "  🧠  Deep work block #2 (90min)"
    echo "  📚  Reading 30min"
    echo ""
    echo "  EVENING (18:00-22:00)"
    echo "  🥘  Light dinner (3h before sleep)"
    echo "  📵  Dim lights, no screens before bed"
    echo "  📓  Journal & plan tomorrow"
    echo ""
    echo "  NIGHT (22:00-06:00)"
    echo "  😴  8+ hours sleep"
    echo ""
    echo "  ⚡  Today's tracker:"
    echo "  Sleep: ___ / 8h  Exercise: ___ min  Energy: ___/10"
    ;;

  filter)
    shift
    if [ $# -eq 0 ]; then
      echo "Usage: opc filter \"your question here\""
      echo "Example: opc filter \"should I freelance full-time?\""
      exit 1
    fi
    QUESTION="$*"
    echo "🔍  5-FILTER DECISION PROTOCOL"
    echo "==============================="
    echo "Question: $QUESTION"
    echo ""
    echo "1️⃣  STRATEGY (Zhang/Lidangzzz): Is this ROI-positive?"
    echo "    □ Yes  □ No  → $(if echo "$QUESTION" | grep -qiE '(cost|pay|money|rent|expensive)'; then echo 'Check: involves money — verify the numbers'; else echo 'No obvious red flag'; fi)"
    echo ""
    echo "2️⃣  FINANCE (Naval/Buffett): Does this compound?"
    echo "    □ Yes  □ No  → $(if echo "$QUESTION" | grep -qiE '(build|create|learn|skill|product)'; then echo 'Check: involves building — good for compounding'; else echo 'Neutral — check moat potential'; fi)"
    echo ""
    echo "3️⃣  HEALTH (Bryan/Huberman): Will this harm you?"
    echo "    □ Yes  □ No  → Check: does this affect sleep/stress?"
    echo ""
    echo "4️⃣  MEDIA (Dan Koe): Can you create from this?"
    echo "    □ Yes  □ No  → Check: is this worth documenting?"
    echo ""
    echo "5️⃣  INNOVATION (Musk): Is there a better way?"
    echo "    □ Yes  □ No  → Check: first principles?"
    echo ""
    echo "Result: 3+ YES = proceed. 3+ NO = stop."
    ;;

  health)
    echo "🧬  HEALTH TRACKER"
    echo "=================="
    echo "Date: $(date +%Y-%m-%d)"
    echo ""
    echo "  MORNING CHECK"
    echo "  ☐ Sunlight before 10am"
    echo "  ☐ No caffeine for 90min after waking"
    echo "  ☐ 500ml water"
    echo ""
    echo "  NUTRITION"
    echo "  ☐ Whole food breakfast"
    echo "  ☐ Protein + veggies lunch"
    echo "  ☐ Dinner 3h before sleep"
    echo ""
    echo "  MOVEMENT"
    echo "  ☐ Exercise today (___ min)"
    echo "  ☐ Walk (___ min)"
    echo "  ☐ Stretch / mobility"
    echo ""
    echo "  SLEEP"
    echo "  ☐ Same bedtime as last night?"
    echo "  ☐ No screens 1h before bed"
    echo "  ☐ Room dark and cool"
    ;;

  status)
    echo "📊  OPC STATUS"
    echo "=============="
    echo ""
    echo "  🏛️  Board: READY"
    echo "  💼  Finance: $(ls "$OPC_DIR/skills/finance/"*.md 2>/dev/null | wc -l) SKILLs loaded"
    echo "  🧬  Health: $(ls "$OPC_DIR/skills/health/"*.md 2>/dev/null | wc -l) SKILLs loaded"
    echo "  📱  Media: $(ls "$OPC_DIR/skills/media/"*.md 2>/dev/null | wc -l) SKILLs loaded"
    echo "  🧠  Strategy: $(ls "$OPC_DIR/skills/strategy/"*.md 2>/dev/null | wc -l) SKILLs loaded"
    echo "  🚀  Innovation: $(ls "$OPC_DIR/skills/innovation/"*.md 2>/dev/null | wc -l) SKILLs loaded"
    echo ""
    echo "  🌐  GitHub: https://github.com/Elimek/opc-board"
    echo "  🏠  Local: $OPC_DIR"
    echo ""
    echo "  ⚡  Next board meeting: Sunday"
    ;;

  help|*)
    echo "🏢  OPC BOARD — One-Person Company CLI"
    echo ""
    echo "Commands:"
    echo "  opc board       Start a board meeting"
    echo "  opc daily       Show daily routine"
    echo "  opc filter <q>  Run 5-filter decision protocol"
    echo "  opc health      Run health tracker checklist"
    echo "  opc status      Show OPC system status"
    echo "  opc help        Show this help"
    echo ""
    echo "Usage: bash opc.sh [command]"
    echo "Example: bash opc.sh filter \"should I take this job?\""
    ;;
esac
