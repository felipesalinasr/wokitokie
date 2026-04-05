#!/bin/bash
# SessionStart hook — ensure voice mode is OFF at the start of every session
rm -f /tmp/claude-voice-active
if [ -f /tmp/claude-thinking.pid ]; then
    pid=$(cat /tmp/claude-thinking.pid)
    if [[ "$pid" =~ ^[0-9]+$ ]]; then
        kill "$pid" 2>/dev/null
    fi
    rm -f /tmp/claude-thinking.pid
fi
pkill -x afplay 2>/dev/null
exit 0
