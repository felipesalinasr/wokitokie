#!/usr/bin/env python3
"""Claude Code Stop hook — speaks the assistant's response via ElevenLabs TTS."""
import json, sys, re, subprocess, tempfile, os, shlex, urllib.request

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_ID = os.environ.get("WOKITOKIE_VOICE_ID", "g2W4HAjKvdW93AmsjsOx")
MODEL_ID = os.environ.get("WOKITOKIE_MODEL_ID", "eleven_turbo_v2_5")


def clean_for_speech(text):
    """Strip markdown so it sounds natural when spoken."""
    text = re.sub(r'```[\s\S]*?```', '. code block omitted. ', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\|', ' ', text)
    text = re.sub(r'-{3,}', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{2,}', '. ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    if len(text) > 1500:
        text = text[:1500] + '... message truncated.'
    return text.strip()


def speak_elevenlabs(text):
    """Send text to ElevenLabs TTS and play the audio."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("xi-api-key", ELEVENLABS_API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "audio/mpeg")

    with urllib.request.urlopen(req, timeout=30) as resp:
        audio = resp.read()

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.write(audio)
    tmp.close()
    return tmp.name


def kill_thinking_sound():
    """Stop the thinking sound loop if running."""
    pidfile = "/tmp/claude-thinking.pid"
    if os.path.exists(pidfile):
        try:
            with open(pidfile) as f:
                pid = f.read().strip()
            if pid.isdigit():
                os.kill(int(pid), 9)
        except Exception:
            pass
        try:
            os.remove(pidfile)
        except OSError:
            pass
    subprocess.run(['pkill', '-x', 'afplay'], capture_output=True)


def main():
    if not os.path.exists("/tmp/claude-voice-active"):
        sys.exit(0)

    if not ELEVENLABS_API_KEY:
        sys.exit(0)

    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    if data.get('stop_hook_active'):
        sys.exit(0)

    message = data.get('last_assistant_message', '')
    if not message:
        sys.exit(0)

    clean = clean_for_speech(message)
    if not clean:
        sys.exit(0)

    kill_thinking_sound()

    try:
        audio_file = speak_elevenlabs(clean)
    except Exception:
        sys.exit(0)

    subprocess.Popen(
        ['bash', '-c', f'afplay {shlex.quote(audio_file)}; rm -f {shlex.quote(audio_file)}'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


if __name__ == '__main__':
    main()
