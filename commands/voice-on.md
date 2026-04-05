---
name: voice-on
description: Enable voice-to-voice mode for this session
---

Enable voice-to-voice mode by creating the flag file. Run this bash command:

touch /tmp/claude-voice-active

Then confirm to the user: "Voice mode is on. I'll speak my responses and you'll hear me thinking. Press Escape in the terminal to cut audio anytime. Say /voice-off to disable."

Check that ELEVENLABS_API_KEY environment variable is set. If not, warn the user: "Warning: ELEVENLABS_API_KEY is not set. TTS won't work. Set it with: export ELEVENLABS_API_KEY=your-key"
