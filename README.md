# Woki Tokie

Voice-to-voice mode for Claude Code. Speak to Claude, hear it think, get spoken responses.

## Install

```bash
claude plugin add github:felipesalinasr/wokitokie
```

Or from npm:

```bash
claude plugin add wokitokie
```

## Setup

1. Set your ElevenLabs API key:

```bash
echo 'export ELEVENLABS_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

2. Generate thinking sound clips:

```
/voice-generate
```

## Usage

```
/voice-on     # start voice mode
/voice-off    # stop voice mode
```

When voice mode is on:
- Claude speaks responses aloud via ElevenLabs TTS
- You hear vocal thinking clips while Claude processes ("Hmm, let me think about that...")
- Every session starts with voice OFF — enable it when you want it

## Optional: Hammerspoon Auto-Submit (macOS)

For full hands-free mode, install [Hammerspoon](https://www.hammerspoon.org) and add this to `~/.hammerspoon/init.lua`:

```lua
require("hs.ipc")

SpaceDownTime = 0
HOLD_THRESHOLD = 1.0
FLAG_FILE = "/tmp/claude-voice-active"

SpaceTap = hs.eventtap.new({hs.eventtap.event.types.keyDown, hs.eventtap.event.types.keyUp}, function(event)
    local keyCode = event:getKeyCode()
    local eventType = event:getType()
    if keyCode ~= 49 then return false end
    local f = io.open(FLAG_FILE, "r")
    if not f then return false end
    f:close()
    local app = hs.application.frontmostApplication()
    if not app then return false end
    local bundleID = app:bundleID()
    if bundleID ~= "com.apple.Terminal" and bundleID ~= "com.googlecode.iterm2" and bundleID ~= "dev.warp.Warp-Stable" then return false end
    if eventType == hs.eventtap.event.types.keyDown then
        if SpaceDownTime == 0 then SpaceDownTime = hs.timer.secondsSinceEpoch() end
        return false
    end
    if eventType == hs.eventtap.event.types.keyUp then
        if SpaceDownTime > 0 then
            local held = hs.timer.secondsSinceEpoch() - SpaceDownTime
            SpaceDownTime = 0
            if held >= HOLD_THRESHOLD then
                hs.timer.doAfter(0.5, function() hs.eventtap.keyStroke({}, "return") end)
            end
        end
        return false
    end
    return false
end)
SpaceTap:start()

-- Escape to cut audio
EscTap = hs.eventtap.new({hs.eventtap.event.types.keyDown}, function(event)
    if event:getKeyCode() ~= 53 then return false end
    local f = io.open(FLAG_FILE, "r")
    if not f then return false end
    f:close()
    local app = hs.application.frontmostApplication()
    if not app then return false end
    local bundleID = app:bundleID()
    if bundleID ~= "com.apple.Terminal" and bundleID ~= "com.googlecode.iterm2" and bundleID ~= "dev.warp.Warp-Stable" then return false end
    os.execute("pkill -9 -x afplay 2>/dev/null")
    local pf = io.open("/tmp/claude-thinking.pid", "r")
    if pf then
        local pid = pf:read("*l")
        pf:close()
        if pid and pid:match("^%d+$") then
            hs.task.new("/bin/kill", nil, {"-9", pid}):start()
        end
        os.remove("/tmp/claude-thinking.pid")
    end
    return false
end)
EscTap:start()
```

This lets you hold Space to dictate and press Escape to cut audio mid-sentence.

## Configuration

| Env Variable | Default | Description |
|---|---|---|
| `ELEVENLABS_API_KEY` | (required) | Your ElevenLabs API key |
| `WOKITOKIE_VOICE_ID` | `g2W4HAjKvdW93AmsjsOx` | ElevenLabs voice ID |
| `WOKITOKIE_MODEL_ID` | `eleven_turbo_v2_5` | ElevenLabs model |

## Requirements

- macOS (uses `afplay` for audio playback)
- Python 3
- [ElevenLabs](https://elevenlabs.io) API key
- Claude Code with voice mode enabled (`voiceEnabled: true` in settings)

## License

MIT
