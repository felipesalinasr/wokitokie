#!/bin/bash
# Play a random vocal thinking clip while Claude processes
[ ! -f /tmp/claude-voice-active ] && exit 0

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(dirname "$0")")")}"
SOUNDS_DIR="$PLUGIN_ROOT/hooks/scripts/thinking-sounds"
PIDFILE="/tmp/claude-thinking.pid"

# Kill any existing thinking sound
if [ -f "$PIDFILE" ]; then
    pid=$(cat "$PIDFILE")
    if [[ "$pid" =~ ^[0-9]+$ ]]; then
        kill "$pid" 2>/dev/null
    fi
    rm -f "$PIDFILE"
fi

# Pick a random sound
SOUNDS=("$SOUNDS_DIR"/*.mp3)
if [ ${#SOUNDS[@]} -eq 0 ]; then
    exit 0
fi
SOUND="${SOUNDS[$((RANDOM % ${#SOUNDS[@]}))]}"

[ ! -f "$SOUND" ] && exit 0

afplay "$SOUND" 2>/dev/null &
echo $! > "$PIDFILE"
