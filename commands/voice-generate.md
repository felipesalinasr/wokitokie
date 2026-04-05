---
name: voice-generate
description: Generate vocal thinking sound clips using ElevenLabs TTS
---

Generate the vocal thinking sound clips that play while Claude is processing. This requires the ELEVENLABS_API_KEY environment variable to be set.

First check if the thinking sounds directory already has mp3 files:
ls ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/thinking-sounds/*.mp3 2>/dev/null

If sounds already exist, ask the user if they want to regenerate them.

Then run:
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/generate-thinking-sounds.py

This generates 15 vocal thinking clips like "Hmm, let me think about that..." using the same ElevenLabs voice that speaks responses. Each clip is different to keep the experience varied.

If it fails, tell the user to check their ELEVENLABS_API_KEY.
