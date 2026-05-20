#!/bin/bash
# First-time setup script
# Run: bash scripts/setup.sh

echo "🚀 OPC Board — Setup"
echo "====================="

# Check for git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Install git first."
    exit 1
fi

# Init git if not already
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git initialized"
fi

echo ""
echo "📋 Next steps:"
echo "1. Create a GitHub repo named 'opc-board'"
echo "2. Run:"
echo "   git add ."
echo "   git commit -m 'Initial commit: OPC Board skeleton'"
echo "   git remote add origin https://github.com/YOUR_USERNAME/opc-board.git"
echo "   git push -u origin main"
echo ""
echo "3. Go to GitHub → Settings → Pages → select main branch / (root)"
echo "4. Wait 2 minutes → your board is live!"
echo ""
echo "Need a custom domain? Edit CNAME file, then set DNS."
