---
name: voice-off
description: Disable voice-to-voice mode
---

Disable voice-to-voice mode. Run these bash commands:

rm -f /tmp/claude-voice-active
pkill -9 -x afplay 2>/dev/null
pid=$(cat /tmp/claude-thinking.pid 2>/dev/null); if [ -n "$pid" ] && echo "$pid" | grep -qE '^[0-9]+$'; then kill "$pid" 2>/dev/null; fi; rm -f /tmp/claude-thinking.pid

Then confirm: "Voice mode is off."
