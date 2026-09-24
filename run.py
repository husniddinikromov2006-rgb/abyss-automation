# ============================================================
# ABYSS SECRETS — SMART CLOUD ENGINE v4
# 100% GITHUB ACTIONS MOSLASHTIRILGAN VARIANT
# ============================================================

import os
import sys
import json
import random
import asyncio
import textwrap
import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

import requests
import edge_tts

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip
)
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ============================================================
# SOZLAMALAR
# ============================================================

# Pexels API Key (agar muhitda bo'lmasa, zaxira kalit ishlatiladi)
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "EdoUks31ZIxOOLAE35gYGpgiP3ikgDFZBiTlmDEievg9OUnR87AGxoLX")

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]

HISTORY_FILE = "history.json"
OUT_DIR = Path("abyss_output")
OUT_DIR.mkdir(exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
FPS = 24
VOICE = "en-US-ChristopherNeural"
MIN_SHORT_SECONDS = 50
PART2_LIKE_GOAL = 500

# ============================================================
# KONTENT BAZASI (OCEAN, COSMOS, US HISTORY, COLD WAR)
# ============================================================

SHORTS = [
    # ---------------- OCEAN ----------------
    {
        "id": "ocean_most_unexplored",
        "topic": "ocean",
        "title": "95% of the Ocean Is Still a Mystery 🌊 #Shorts",
        "hook": "We have mapped the Moon better than parts of our own ocean.",
        "script": (
            "We have mapped the Moon better than parts of our own ocean. "
            "Thousands of meters below the surface, sunlight disappears, "
            "pressure becomes extreme, and entire ecosystems survive without sunlight. "
            "Scientists keep finding creatures and environments that look almost alien. "
            "And the deeper we go, the more questions appear. "
            "So what do you think is still hiding down there?"
        ),
        "queries": [
            "deep ocean underwater mysterious",
            "deep sea creature dark",
            "underwater trench expedition",
            "bioluminescent jellyfish ocean",
            "submarine deep ocean"
        ],
        "cta": "Follow Abyss Secrets for the next dive into the unknown."
    },
    {
        "id": "ocean_bioluminescence",
        "topic": "ocean",
        "title": "The Ocean Lights Up in Total Darkness 😳🌊 #Shorts",
        "hook": "Imagine turning off every light... and the ocean starts glowing.",
        "script": (
            "Imagine turning off every light and the ocean starts glowing. "
            "Far below the surface, many organisms produce their own light through bioluminescence. "
            "Some use it to attract prey. Others use it to confuse predators or communicate. "
            "In complete darkness, tiny flashes can look like an underwater galaxy. "
            "And this is happening all around us, far below the waves."
        ),
        "queries": [
            "bioluminescent plankton ocean",
            "glowing jellyfish deep sea",
            "deep sea blue lights",
            "underwater night ocean",
            "bioluminescent sea creature"
        ],
        "cta": "Subscribe if you want to see what lives beneath the surface."
    },
    {
        "id": "ocean_mariana_pressure",
        "topic": "ocean",
        "title": "What Happens at the Bottom of the Mariana Trench? 🌊 #Shorts",
        "hook": "At the deepest ocean trenches, the pressure is almost unimaginable.",
        "script": (
            "At the deepest ocean trenches, the pressure is almost unimaginable. "
            "The Mariana Trench reaches nearly eleven kilometers below sea level. "
            "Down there, there is no sunlight, the water is near freezing, "
            "and the pressure is enormous. Yet life still exists. "
            "Tiny organisms and strange animals have adapted to conditions that seem impossible. "
            "The real mystery is not whether life can survive there, but how much we still have not seen."
        ),
        "queries": [
            "Mariana trench deep sea",
            "deep ocean trench submarine",
            "hadal zone underwater",
            "deep sea creature",
            "ocean abyss"
        ],
        "cta": "Abyss Secrets — deeper than the surface."
    },

    # ---------------- COSMOS ----------------
    {
        "id": "cosmos_black_hole",
        "topic": "cosmos",
        "title": "What Would Happen If You Got Near a Black Hole? 🕳️🌌 #Shorts",
        "hook": "A black hole does not need to touch you to change your view of time.",
        "script": (
            "A black hole does not need to touch you to change your view of time. "
            "Its gravity is so strong that light itself can be trapped beyond the event horizon. "
            "From far away, an object approaching the horizon can appear to slow down dramatically. "
            "Near the black hole, space and time behave in ways that challenge everyday intuition. "
            "And the strangest part is that we still cannot directly see the inside."
        ),
        "queries": [
            "black hole space cinematic",
            "galaxy black hole",
            "deep space stars",
            "accretion disk black hole",
            "cosmic nebula"
        ],
        "cta": "Follow Abyss Secrets for more journeys into the unknown."
    },
    {
        "id": "cosmos_space_silence",
        "topic": "cosmos",
        "title": "Why Is Space So Silent? 🌌 #Shorts",
        "hook": "The universe can explode with unimaginable energy... and you would hear nothing.",
        "script": (
            "The universe can release unimaginable amounts of energy, yet space itself is silent. "
            "Sound needs a medium such as air or water to travel. "
            "Most of space is an almost perfect vacuum, so ordinary sound waves cannot move through it. "
            "Astronomers can still detect other signals, including radio waves and light. "
            "So the universe is not truly quiet — we simply need different senses to listen."
        ),
        "queries": [
            "deep space galaxy stars",
            "astronaut space cinematic",
            "nebula universe",
            "satellite earth space",
            "cosmic stars"
        ],
        "cta": "If space fascinates you, stay with Abyss Secrets."
    },
    {
        "id": "cosmos_neutron_star",
        "topic": "cosmos",
        "title": "A Star Can Become Smaller Than a City 🤯🌌 #Shorts",
        "hook": "Imagine compressing more mass than the Sun into something city-sized.",
        "script": (
            "Imagine compressing more mass than the Sun into an object roughly the size of a city. "
            "That is the extreme world of neutron stars. "
            "They can form after massive stars explode and their cores collapse. "
            "The remaining matter becomes extraordinarily dense. "
            "Some neutron stars rotate rapidly and send beams of radiation through space like cosmic lighthouses."
        ),
        "queries": [
            "neutron star space",
            "supernova explosion",
            "pulsar space",
            "galaxy stars cinematic",
            "deep universe"
        ],
        "cta": "Subscribe for the next cosmic mystery."
    },

    # ---------------- U.S. HISTORY ----------------
    {
        "id": "us_history_d_day",
        "topic": "us_history",
        "title": "June 6, 1944: The Normandy Secret Plan 🇺🇸 #Shorts",
        "hook": "Before sunrise, the single greatest airborne invasion in history began.",
        "script": (
            "Before sunrise on June 6, 1944, Allied forces began the Normandy invasion, "
            "known as D-Day and part of Operation Overlord. The operation was a massive "
            "multinational effort and opened the Western Front in Europe. Before the landing, "
            "weather, timing and planning created enormous uncertainty. General Dwight Eisenhower "
            "even prepared a secret statement accepting responsibility if the invasion failed."
        ),
        "queries": [
            "historical military aerial",
            "old military map Europe",
            "1940s vintage aircraft",
            "historic ocean coastline",
            "vintage military landscape"
        ],
        "cta": "Follow for the next declassified historical chapter."
    },
    {
        "id": "us_history_pearl_harbor",
        "topic": "us_history",
        "title": "December 7, 1941: The Strike at Dawn 🇺🇸 #Shorts",
        "hook": "In less than two hours, American history changed forever.",
        "script": (
            "On December 7, 1941, naval and air forces struck Pearl Harbor in Hawaii. "
            "The surprise attack caused catastrophic losses and immediately altered the course of World War Two. "
            "The following day, President Franklin Roosevelt addressed a stunned Congress. "
            "Pearl Harbor remains one of the most critical turning points in human history."
        ),
        "queries": [
            "harbor aerial historical",
            "vintage naval warship ocean",
            "old newspaper archive",
            "historical island landscape",
            "clouds smoke sky cinematic"
        ],
        "cta": "Follow for more documented history stories."
    },

    # ---------------- COLD WAR / DECLASSIFIED ----------------
    {
        "id": "us_politics_cuban_crisis",
        "topic": "us_politics_history",
        "title": "13 Days That Almost Ended the World 🇺🇸🌎 #Shorts",
        "hook": "For thirteen days in 1962, humanity stood inches away from nuclear annihilation.",
        "script": (
            "In October 1962, U-2 spy plane photos revealed Soviet nuclear missiles in Cuba. "
            "For thirteen days, President Kennedy and his advisors debated naval blockades and airstrikes, "
            "while Soviet submarines patrolled the Atlantic armed with nuclear torpedoes. "
            "It was the closest the world ever came to absolute destruction."
        ),
        "queries": [
            "vintage radar military",
            "submarine ocean dark",
            "Cold War historical documents",
            "military map tactical",
            "vintage naval fleet"
        ],
        "cta": "Follow for the next Cold War declassified file."
    }
]

# ============================================================
# TARIX VA ANALITIKA
# ============================================================

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {
            "uploaded_ids": [],
            "video_stats": {},
            "topic_views": {"ocean": 0, "cosmos": 0, "us_history": 0, "us_politics_history": 0},
        }
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("uploaded_ids", [])
        data.setdefault("video_stats", {})
        data.setdefault("topic_views", {"ocean": 0, "cosmos": 0, "us_history": 0, "us_politics_history": 0})
        return data
    except Exception:
        return {
            "uploaded_ids": [],
            "video_stats": {},
            "topic_views": {"ocean": 0, "cosmos": 0, "us_history": 0, "us_politics_history": 0},
        }

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def choose_story():
    history = load_history()
    uploaded = set(history.get("uploaded_ids", []))
    available = [s for s in SHORTS if s["id"] not in uploaded]

    if not available:
        # Barchasi tugasa, tarixni qaytadan boshlaymiz
        history["uploaded_ids"] = []
        save_history(history)
        available = SHORTS

    return random.choice(available)

# ============================================================
# YOUTUBE AUTH
# ============================================================

def get_youtube_service():
    creds = None
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception:
            creds = None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if not os.path.exists("client_secret.json"):
            raise FileNotFoundError("client_secret.json topilmadi.")
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

# ============================================================
# OVOZ VA PEXELS
# ============================================================

async def generate_voice(text, filename):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="-6%",
        pitch="-1Hz"
    )
    await communicate.save(filename)

def search_pexels(query, per_page=10):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(
        url,
        headers=headers,
        params={"query": query, "orientation": "portrait", "per_page": per_page},
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("videos", [])

def download_one_pexels(query, output_file):
    try:
        videos = search_pexels(query)
    except Exception:
        videos = []

    if not videos:
        fallback_queries = ["deep ocean underwater", "space stars universe", "galaxy nebula"]
        videos = search_pexels(random.choice(fallback_queries))

    random.shuffle(videos)
    video = videos[0]
    files = video.get("video_files", [])

    vertical = [f for f in files if f.get("height", 0) > f.get("width", 0)]
    selected = max(vertical, key=lambda x: x.get("width", 0)) if vertical else max(files, key=lambda x: x.get("width", 0))
    link = selected["link"]

    with requests.get(link, stream=True, timeout=60) as response:
        response.raise_for_status()
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

def crop_to_vertical(clip):
    w, h = clip.size
    target_ratio = WIDTH / HEIGHT
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        x1 = int((w - new_w) / 2)
        clip = clip.crop(x1=x1, y1=0, x2=x1 + new_w, y2=h)
    else:
        new_h = int(w / target_ratio)
        y1 = int((h - new_h) / 2)
        clip = clip.crop(x1=0, y1=y1, x2=w, y2=y1 + new_h)

    return clip.resize((WIDTH, HEIGHT))

def build_multiscene_short(story, voice_file, output_file):
    audio = AudioFileClip(voice_file)
    total_duration = max(audio.duration, MIN_SHORT_SECONDS)
    queries = story["queries"]
    scene_count = min(5, len(queries))
    scene_duration = total_duration / scene_count

    clips = []
    temp_files = []

    try:
        for i in range(scene_count):
            query = queries[i]
            raw_file = OUT_DIR / f"scene_{i}.mp4"
            temp_files.append(raw_file)
            print(f"🎥 Sahna {i+1}/{scene_count}: {query}")

            download_one_pexels(query, str(raw_file))
            clip = VideoFileClip(str(raw_file))
            clip = crop_to_vertical(clip)

            if clip.duration < scene_duration:
                clip = clip.loop(duration=scene_duration)
            else:
                max_start = max(0, clip.duration - scene_duration)
                start = random.uniform(0, max_start) if max_start > 0 else 0
                clip = clip.subclip(start, start + scene_duration)

            clip = clip.set_duration(scene_duration)
            clips.append(clip)

        video = concatenate_videoclips(clips, method="compose")
        video = video.subclip(0, min(video.duration, total_duration))
        video = video.set_audio(audio)
        video = video.set_duration(audio.duration)

        video.write_videofile(
            str(output_file),
            codec="libx264",
            audio_codec="aac",
            fps=FPS,
            preset="ultrafast",
            threads=4,
            verbose=False,
            logger=None,
        )

        audio.close()
        video.close()
        for c in clips:
            c.close()
    finally:
        for p in temp_files:
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass

# ============================================================
# YUKLASH PIPELINE
# ============================================================

def upload_to_youtube(youtube, story, video_path):
    title = story["title"]
    description = (
        f"{story['script']}\n\n"
        f"{story['cta']}\n"
        f"If this reaches {PART2_LIKE_GOAL} likes, Part 2 continues the story.\n\n"
        "Abyss Secrets explores deep-ocean mysteries, cosmic phenomena, and historical secrets.\n\n"
        "#Shorts #AbyssSecrets #DeepSea #Space #Mystery #History"
    )

    tags = ["Abyss Secrets", "Shorts", "deep sea", "ocean mystery", "space mystery", "cosmos", "history", "mystery"]

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "28",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    result = request.execute()
    video_id = result["id"]

    history = load_history()
    history.setdefault("uploaded_ids", []).append(story["id"])
    history.setdefault("video_stats", {})[story["id"]] = video_id
    save_history(history)

    print("=" * 60)
    print(f"🚀 YUKLANDI: {title}")
    print(f"🔗 Havola: https://youtu.be/{video_id}")
    print("=" * 60)
    return video_id

def run_short():
    youtube = get_youtube_service()
    story = choose_story()
    print(f"\n🎯 MAVZU: {story['topic'].upper()} | {story['title']}")

    narration = story["script"].strip() + " " + story["cta"].strip() + f" If this video reaches {PART2_LIKE_GOAL} likes, we will uncover part two."
    voice_file = OUT_DIR / f"{story['id']}_voice.mp3"
    final_file = OUT_DIR / f"{story['id']}_short.mp4"

    asyncio.run(generate_voice(narration, str(voice_file)))
    build_multiscene_short(story, voice_file, final_file)
    upload_to_youtube(youtube, story, final_file)

if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "short"
    if mode == "auth":
        get_youtube_service()
        print("✅ OAuth tayyor.")
    else:
        run_short()