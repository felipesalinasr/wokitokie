#!/usr/bin/env python3
"""Generate vocal thinking clips using ElevenLabs TTS."""
import json, os, urllib.request, time

API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_ID = "g2W4HAjKvdW93AmsjsOx"
MODEL_ID = "eleven_turbo_v2_5"
OUTPUT_DIR = os.path.expanduser("~/.claude/hooks/thinking-sounds")

PHRASES = [
    {"name": "think-01", "text": "Hmm... let me think about that for a moment."},
    {"name": "think-02", "text": "Okay... I'm looking through a few options here."},
    {"name": "think-03", "text": "Interesting... let me dig into this."},
    {"name": "think-04", "text": "Mmm... give me a second, I'm working through something."},
    {"name": "think-05", "text": "Alright... I'm evaluating a couple of approaches."},
    {"name": "think-06", "text": "Hmm... that's a good one. Let me figure this out."},
    {"name": "think-07", "text": "Okay, okay... I think I see where this is going."},
    {"name": "think-08", "text": "Let me check something real quick..."},
    {"name": "think-09", "text": "Mmhmm... I'm putting the pieces together."},
    {"name": "think-10", "text": "Oh, interesting... hold on, let me work through this."},
    {"name": "think-11", "text": "Right... so there's a few ways to do this."},
    {"name": "think-12", "text": "Hmm... almost there, just thinking it through."},
    {"name": "think-13", "text": "One sec... I want to make sure I get this right."},
    {"name": "think-14", "text": "Okay, so... let me consider the options here."},
    {"name": "think-15", "text": "Mmm... yeah, I think I know what to do. Give me a moment."},
]

if not API_KEY:
    print("Error: ELEVENLABS_API_KEY env var not set")
    exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

for phrase in PHRASES:
    outpath = os.path.join(OUTPUT_DIR, f"{phrase['name']}.mp3")
    if os.path.exists(outpath):
        print(f"  skip {phrase['name']} (exists)")
        continue

    print(f"  generating {phrase['name']}: {phrase['text']}")
    payload = json.dumps({
        "text": phrase["text"],
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.35,
            "similarity_boost": 0.75,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        data=payload,
        method="POST",
    )
    req.add_header("xi-api-key", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "audio/mpeg")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio = resp.read()
        with open(outpath, "wb") as f:
            f.write(audio)
        print(f"  saved ({len(audio)} bytes)")
    except Exception as e:
        print(f"  FAILED: {e}")

    time.sleep(0.5)

print("done")
