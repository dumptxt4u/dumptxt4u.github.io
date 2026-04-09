#!/bin/bash

echo "============================================"
echo "   📚 BookShelf Library Manager Launcher"
echo "============================================"

# Kill any existing process on port 5005
echo "🔍 Checking port 5005..."
PID=$(lsof -ti:5005 2>/dev/null)

if [ -n "$PID" ]; then
    echo "🛑 Found running process (PID: $PID). Killing it..."
    kill -9 $PID
    sleep 1.5
    echo "✅ Old process terminated."
else
    echo "✅ Port 5005 is free."
fi

# Get local IP address
IP=$(hostname -I | awk '{print $1}')
if [ -z "$IP" ]; then
    IP="127.0.0.1"
fi

echo ""
echo "🚀 Starting BookShelf Server..."
echo "🌐 Local Access     : http://127.0.0.1:5005"
echo "🌐 Network Access   : http://$IP:5005"
echo ""
echo "📱 Open this address on your phone or other devices:"
echo "   → http://$IP:5005"
echo "============================================"

# Start the Flask app
python3 app.py
