#!/bin/bash
# Quick start script for Classroom Manager with Network Support

set -e

echo "🎓 Classroom Manager - Network Setup Script"
echo "=========================================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Navigate to project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/lab_manager"

echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "✅ Dependencies installed"
echo ""
echo "=========================================="
echo "Setup Options:"
echo ""
echo "1) Start Server (GUI) - Recommended"
echo "   python -m server.gui.main_window"
echo ""
echo "2) Start Agent on Workstation"
echo "   python -m agent.main"
echo ""
echo "3) Test Network Discovery"
echo "   python -c 'from server.network_discovery import discover_agents_sync; print(discover_agents_sync())'"
echo ""
echo "=========================================="
echo ""
echo "For detailed setup instructions, see:"
echo "  - NETWORK_SETUP_RU.md (Russian)"
echo "  - NETWORK_SETUP_EN.md (English)"

