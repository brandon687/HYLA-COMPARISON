#!/bin/bash
echo "========================================="
echo "HYLA Stock Comparison - Server Status"
echo "========================================="
echo ""

# Check if server is running
if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
    echo "✅ Server is RUNNING"
    echo "🌐 URL: http://localhost:5001"
    echo ""
    echo "Health Check:"
    curl -s http://localhost:5001/api/health | python3 -m json.tool
    echo ""
    echo "✨ Ready to use! Open the URL in your browser."
else
    echo "❌ Server is NOT running"
    echo ""
    echo "To start the server, run:"
    echo "  python3 web_app.py"
fi
echo ""
echo "========================================="
