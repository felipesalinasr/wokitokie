-- Enable CLI access
require("hs.ipc")

-- Voice-to-voice auto-submit for Claude Code
-- Only active when /tmp/claude-voice-active exists

SpaceDownTime = 0
HOLD_THRESHOLD = 1.0 -- seconds
FLAG_FILE = "/tmp/claude-voice-active"

VoiceLog = hs.logger.new("voice", "debug")

SpaceTap = hs.eventtap.new({hs.eventtap.event.types.keyDown, hs.eventtap.event.types.keyUp}, function(event)
    local keyCode = event:getKeyCode()
    local eventType = event:getType()

    -- Space key = keycode 49
    if keyCode ~= 49 then return false end

    -- Check if voice mode is active
    local f = io.open(FLAG_FILE, "r")
    if not f then return false end
    f:close()

    -- Only act when Terminal is frontmost
    local app = hs.application.frontmostApplication()
    if not app then return false end
    local bundleID = app:bundleID()

    if bundleID ~= "com.apple.Terminal"
       and bundleID ~= "com.googlecode.iterm2"
       and bundleID ~= "dev.warp.Warp-Stable" then
        return false
    end

    if eventType == hs.eventtap.event.types.keyDown then
        if SpaceDownTime == 0 then
            SpaceDownTime = hs.timer.secondsSinceEpoch()
        end
        return false
    end

    if eventType == hs.eventtap.event.types.keyUp then
        if SpaceDownTime > 0 then
            local held = hs.timer.secondsSinceEpoch() - SpaceDownTime
            SpaceDownTime = 0
            if held >= HOLD_THRESHOLD then
                hs.timer.doAfter(0.5, function()
                    hs.eventtap.keyStroke({}, "return")
                end)
            end
        end
        return false
    end

    return false
end)

SpaceTap:start()

-- Escape key kills voice playback instantly (thinking + TTS)
-- Only active when voice mode is on and terminal is focused
EscTap = hs.eventtap.new({hs.eventtap.event.types.keyDown}, function(event)
    local keyCode = event:getKeyCode()

    -- Escape = keycode 53
    if keyCode ~= 53 then return false end

    -- Only when voice mode is active
    local f = io.open(FLAG_FILE, "r")
    if not f then return false end
    f:close()

    -- Only in terminal apps
    local app = hs.application.frontmostApplication()
    if not app then return false end
    local bundleID = app:bundleID()

    if bundleID ~= "com.apple.Terminal"
       and bundleID ~= "com.googlecode.iterm2"
       and bundleID ~= "dev.warp.Warp-Stable" then
        return false
    end

    -- Kill all audio playback
    os.execute("pkill -9 -x afplay 2>/dev/null")

    -- Kill thinking sound process safely (validate PID before killing)
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
hs.alert.show("Hammerspoon ready")
