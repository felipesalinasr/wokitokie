# Woki Tokie

Voice-to-voice system for Claude Code. Hold Space to dictate, release to auto-submit, hear Claude's response spoken back.

## Architecture

Three systems work together, all gated by `/tmp/claude-voice-active`:

1. **ElevenLabs TTS** (`hooks/speak-response.py`) — Stop hook speaks Claude's response
2. **Hammerspoon auto-submit** (`hammerspoon/init.lua`) — Space held >1s in terminal auto-presses Enter
3. **Thinking sounds** (`hooks/start-thinking.sh`) — loops audio while Claude processes

## Activation

- **OFF by default** — every session starts silent via `hooks/kill-voice.sh` (SessionStart hook)
- Enable: `touch /tmp/claude-voice-active`
- Disable: `rm /tmp/claude-voice-active`

## Installation

### 1. Copy hooks to `~/.claude/hooks/`

```bash
cp hooks/speak-response.py ~/.claude/hooks/
cp hooks/start-thinking.sh ~/.claude/hooks/
cp hooks/kill-voice.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/start-thinking.sh ~/.claude/hooks/kill-voice.sh
```

### 2. Add hooks to `~/.claude/settings.json`

Merge the contents of `settings-hooks.example.json` into your settings.

### 3. Install Hammerspoon config

```bash
cp hammerspoon/init.lua ~/.hammerspoon/init.lua
```

Reload Hammerspoon.

### 4. Set your ElevenLabs API key

```bash
export ELEVENLABS_API_KEY="your-key-here"
```

Or set it in `~/.zshrc`.

### 5. Add a thinking sound

Place a `thinking.mp3` file at `~/.claude/hooks/thinking.mp3`.

## Configuration

- **Voice ID**: Change `VOICE_ID` in `speak-response.py` (default: Rachel)
- **Model**: Change `MODEL_ID` (default: `eleven_turbo_v2_5`)
- **Hold threshold**: Change `HOLD_THRESHOLD` in `init.lua` (default: 1.0s)
- **Auto-submit delay**: Change the `doAfter` timer in `init.lua` (default: 0.5s)

## Requirements

- macOS
- Claude Code CLI with voice mode (`voiceEnabled: true`)
- [ElevenLabs](https://elevenlabs.io) API key
- [Hammerspoon](https://www.hammerspoon.org)
- Python 3
