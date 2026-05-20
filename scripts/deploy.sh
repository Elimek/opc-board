#!/bin/bash
# Local deploy script — serves the static site for testing
# Usage: bash scripts/deploy.sh

echo "🔧 OPC Board — Local Dev Server"
echo "==============================="
echo ""
echo "Option 1: Python (built-in)"
echo "  python -m http.server 8000"
echo "  → http://localhost:8000"
echo ""
echo "Option 2: Node.js live-server"
echo "  npx live-server --port=8000"
echo "  → http://localhost:8000"
echo ""
echo "Option 3: VS Code Live Preview"
echo "  Right-click index.html → Open with Live Server"
echo ""
echo "For GitHub Pages deployment:"
echo "  1. Push to GitHub"
echo "  2. Settings → Pages → Source: main branch / (root)"
echo "  3. Wait 2 minutes"
echo "  4. → https://YOUR_USERNAME.github.io/opc-board"
