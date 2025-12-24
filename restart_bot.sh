#!/bin/bash

# Restart bot script - Aggressive version

echo "🔄 Restarting Property Collection Bot..."

# Keep finding and killing until none left
while true; do
    PID=$(ps aux | grep "python3 bot.py" | grep -v grep | awk '{print $2}')
    
    if [ -z "$PID" ]; then
        break
    fi
    
    echo "   Stopping existing bot (PID: $PID)..."
    kill -9 $PID 2>/dev/null
    sleep 1
done

# Start bot in background
echo "   Starting bot..."
nohup python3 bot.py > bot.log 2>&1 &

echo "✅ Bot restarted successfully!"
echo "   Check logs: tail -f bot.log"
