# ============================================================
# ABYSS SECRETS — BULLETPROOF HORROR PIPELINE v9 (STABLE)
# PILLOW, NETWORK RETRY, ANTI-BAN VA DAHSHATLI OKEAN MONTAJI
# ============================================================

import os
import sys
import json
import time
import random
import asyncio
import numpy as np
from pathlib import Path

# --- PILLOW ANTIALIAS FIX (Python 3.10+ / 3.13+ uchun) ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    if hasattr(PIL.Image, 'Resampling'):
        PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
    else:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# --------------------------------------------------------

import requests
import edge_tts

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    AudioClip,
    CompositeAudioClip,
)
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ============================================================
# ASOSIY SOZLAMALAR
# ============================================================

PEXELS_API_KEY = os.environ.get(
    "PEXELS_API_KEY",
    "EdoUks31ZIxOOLAE35gYGpgiP3ikgDFZBiTlmDEievg9OUnR87AGxoLX"
)

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
MIN_SHORT_SECONDS = 52
PART2_LIKE_GOAL = 500

# ============================================================
# HORROR MATRITSA BAZASI
# ============================================================

HORROR_ZONES = [
    {"name": "the pitch-black Mariana Abyss", "depth": "36,000 feet into complete darkness"},
    {"name": "the Devil's Sea Graveyard", "depth": "24,000 feet below storm waters"},
    {"name": "Point Nemo Oceanic Void", "depth": "the most remote chasm on Earth"},
    {"name": "the Antarctic Sub-Zero Trench", "depth": "sub-glacial hydrothermal vents"},
    {"name": "the Puerto Rico Trench Abyss", "depth": "28,000 feet into crushing pressure"}
]

HORROR_TARGETS = [
    {"vessel": "a titanium military submarine", "failure": "decompression warning sirens echoing in the hull"},
    {"vessel": "a deep-sea salvage team", "failure": "underwater optical feeds cutting to static one by one"},
    {"vessel": "a covert naval destroyer", "failure": "the forward sonar dome violently crushed from below"},
    {"vessel": "an isolated sub-sea exploration probe", "failure": "heavy steel mooring cables snapping instantly"}
]

HORROR_CREATURES = [
    {
        "terror_name": "THE TRENCH DEVOURER",
        "intro": "a colossal nightmare measuring nearly two hundred feet with translucent jaws",
        "strike": "surged from the freezing abyss, crushing external pressure hulls instantly",
        "aftermath": "leaving deep acidic puncture wounds and unknown biological residue across the wreckage"
    },
    {
        "terror_name": "ANOMALY KRAKEN ZERO",
        "intro": "a massive barbed predator that hunts through ultra-low acoustic pulses",
        "strike": "wrapped armored tentacles lined with razor bone hooks around the main propellers",
        "aftermath": "dragging the entire vessel downward past critical crush-depth in under ninety seconds"
    },
    {
        "terror_name": "THE BLACK ABYSS LEVIATHAN",
        "intro": "a prehistoric apex horror whose bite force exceeds forty tons per square inch",
        "strike": "rammed the forward observation bridge, shattering reinforced quartz portholes",
        "aftermath": "leaving the vessel flooded in freezing pitch-black seawater as emergency alarms blared"
    },
    {
        "terror_name": "FAST MOVER PHANTOM",
        "intro": "an intelligent bio-mechanical organism emitting terrifying ultrasonic screams",
        "strike": "circled the vessel at two hundred knots before severing all communication lines",
        "aftermath": "causing complete electrical failure moments before sonar captured its jaws opening wide"
    }
]

HORROR_QUERY_POOLS = [
    [
        "scary deep ocean monster dark water horror",
        "underwater dark red emergency lights submarine",
        "giant monster jaws underwater terrifying",
        "giant squid attacking ship dark storm horror",
        "abyss ocean deep dark glowing eyes scary"
    ],
    [
        "scary sea creature teeth dark waters",
        "submarine emergency alarm red flashing dark",
        "terrifying deep sea predator 3d animation",
        "underwater wreckage dark trench horror",
        "sonar display dark green horror military"
    ],
    [
        "scary sea monster silhouette giant ocean",
        "dark waters underwater horror cinematic",
        "underwater abyss terrifying chasm",
        "creature stalking submarine dark lights",
        "storm waves dark ocean night scary"
    ]
]

def generate_horror_story(history):
    uploaded = set(history.get("uploaded_ids", []))

    for _ in range(500):
        zone = random.choice(HORROR_ZONES)
        target = random.choice(HORROR_TARGETS)
        beast = random.choice(HORROR_CREATURES)
        year = random.randint(1979, 2024)
        part = random.choice([1, 2])

        story_id = f"horror_{beast['terror_name'][:4]}_{year}_p{part}".lower().replace(" ", "_")
        if story_id not in uploaded:
            break
    else:
        story_id = f"horror_abyss_{random.randint(100000, 999999)}"

    if part == 1:
        title = f"TERRIFYING: {beast['terror_name']} Attack at {zone['depth'][:12]} (Part 1) 🚨🦑 #Shorts"
        hook = f"In {year}, {target['vessel']} plunged into {zone['name']}... and encountered something impossible."
        script = (
            f"Do not watch this in the dark. In {year}, {target['vessel']} descended into {zone['name']}, "
            f"reaching {zone['depth']}. Without warning, {target['failure']}. "
            f"External searchlights cut through the pitch-black water, illuminating {beast['intro']}. "
            f"Before anyone could scream, the entity {beast['strike']}! "
            f"Declassified military audio captured pure panic as titanium shrieked and hull seals tore apart."
        )
        cta = "Part 2 contains the final recovered audio log. Like and subscribe if you dare to see Part 2."
    else:
        title = f"THE TRUTH: What Destroyed {target['vessel'][:22]} (Part 2) ☠️🌊 #Shorts"
        hook = f"Officials blamed water pressure, but black-box data revealed a deep ocean horror."
        script = (
            f"Part two. When search teams reached the shattered wreckage inside {zone['name']}, "
            f"the hull had not collapsed from pressure — it had been violently shredded from the outside. "
            f"Investigators found {beast['aftermath']}. "
            f"The final telemetry recorded sickening feeding sounds in total darkness before power died completely. "
            f"Ninety-five percent of our oceans remain unexplored, and leviathans far worse than our nightmares are hunting down there."
        )
        cta = "Follow Abyss Secrets if you are brave enough to explore the abyss."

    queries = random.choice(HORROR_QUERY_POOLS)

    return {
        "id": story_id,
        "title": title,
        "hook": hook,
        "script": script,
        "queries": queries,
        "cta": cta
    }

# ============================================================
# TARIXNI SAQLASH
# ============================================================

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {"uploaded_ids": [], "video_stats": {}}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("uploaded_ids", [])
        data.setdefault("video_stats", {})
        return data
    except Exception:
        return {"uploaded_ids": [], "video_stats": {}}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

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
# DAHSHATLI OVOZ VA HORROR SOUNDSCAPE
# ============================================================

async def generate_voice(text, filename):
    # Anti-bot: har safar ovoz tezligi va tempi ozgina farq qiladi
    rates = ["+1%", "+2%", "+3%"]
    pitches = ["-2Hz", "-3Hz", "-4Hz"]
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=random.choice(rates),
        pitch=random.choice(pitches)
    )
    await communicate.save(str(filename))

def make_horror_soundscape(duration):
    sample_rate = 44100

    def make_frame(t):
        heart_rate = 1.35
        heartbeat = np.sin(2 * np.pi * 45.0 * t) * np.maximum(0, np.sin(2 * np.pi * heart_rate * t)) ** 8 * 0.45
        drone1 = np.sin(2 * np.pi * 38.0 * t) * 0.25
        drone2 = np.sin(2 * np.pi * 49.5 * t) * 0.20
        screech = np.sin(2 * np.pi * 120.0 * t + np.sin(2 * np.pi * 2.0 * t)) * 0.08
        audio = (heartbeat + drone1 + drone2 + screech) * 0.22
        return np.vstack((audio, audio)).T

    return AudioClip(make_frame, duration=duration, fps=sample_rate)

# ============================================================
# RESILIENT PEXELS DOWNLOADER
# ============================================================

def search_pexels(query, per_page=12):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    for _ in range(3):
        try:
            response = requests.get(
                url,
                headers=headers,
                params={"query": query, "orientation": "portrait", "per_page": per_page},
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get("videos", [])
        except Exception:
            time.sleep(2)
    return []

def download_one_pexels(query, output_file):
    max_retries = 4
    for attempt in range(max_retries):
        try:
            videos = search_pexels(query)
            if not videos:
                fallback = ["scary monster underwater dark horror", "submarine emergency red light", "dark deep ocean horror"]
                videos = search_pexels(random.choice(fallback))

            if not videos:
                time.sleep(2)
                continue

            random.shuffle(videos)
            video = videos[0]
            files = video.get("video_files", [])

            vertical = [f for f in files if f.get("height", 0) > f.get("width", 0)]
            selected = max(vertical, key=lambda x: x.get("width", 0)) if vertical else max(files, key=lambda x: x.get("width", 0))
            link = selected["link"]

            with requests.get(link, stream=True, timeout=60) as response:
                response.raise_for_status()
                with open(str(output_file), "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

            if os.path.exists(output_file) and os.path.getsize(output_file) > 10000:
                return
        except Exception as e:
            print(f"⚠️ Tarmoq xatosi (urinish {attempt + 1}/{max_retries}): {e}")
            time.sleep(3)

    raise ConnectionError("Pexels serveridan video yuklab bo'lmadi. Internet aloqasini tekshiring.")

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

# ============================================================
# HORROR MONTAJ (PILLOW XATOSIZ)
# ============================================================

def build_horror_short(story, voice_file, output_file):
    voice_audio = AudioFileClip(str(voice_file))
    total_duration = max(voice_audio.duration, MIN_SHORT_SECONDS)

    horror_audio = make_horror_soundscape(total_duration)
    final_audio = CompositeAudioClip([voice_audio, horror_audio])

    queries = story["queries"]
    scene_count = min(5, len(queries))
    scene_duration = total_duration / scene_count

    clips = []
    temp_files = []

    try:
        for i in range(scene_count):
            query = queries[i]
            raw_file = OUT_DIR / f"scene_{story['id']}_{i}.mp4"
            temp_files.append(raw_file)
            print(f"🩸 Dahshatli Sahna {i + 1}/{scene_count}: {query}")

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

        base_video = concatenate_videoclips(clips, method="compose")
        base_video = base_video.subclip(0, min(base_video.duration, total_duration))
        base_video = base_video.set_audio(final_audio)
        base_video = base_video.set_duration(final_audio.duration)

        base_video.write_videofile(
            str(output_file),
            codec="libx264",
            audio_codec="aac",
            fps=FPS,
            preset="ultrafast",
            threads=4,
            verbose=False,
            logger=None,
        )

        voice_audio.close()
        horror_audio.close()
        base_video.close()
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
# XAVFSIZ YOUTUBE YUKLASH (ANTI-SPAM METADATA)
# ============================================================

def upload_to_youtube(youtube, title, description, tags, video_path):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        },
    }
    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    result = request.execute()
    video_id = result["id"]
    print("=" * 60)
    print(f"🚀 DAHSHATLI VIDEO YUKLANDI: {title}")
    print(f"🔗 Havola: https://youtu.be/{video_id}")
    print("=" * 60)
    return video_id

def run_short():
    youtube = get_youtube_service()
    history = load_history()

    story = generate_horror_story(history)
    print(f"\n⚠️ DAHSHAT MAVZUSI ISHGA TUSHDI: {story['title']}")

    narration = (
        story["script"].strip() + " " + story["cta"].strip()
        + f" If this video reaches {PART2_LIKE_GOAL} likes, we will uncover part two."
    )
    voice_file = OUT_DIR / f"{story['id']}_voice.mp3"
    final_file = OUT_DIR / f"{story['id']}_short.mp4"

    asyncio.run(generate_voice(narration, str(voice_file)))
    build_horror_short(story, str(voice_file), str(final_file))

    # Toza va spam bo'lmagan metadata (Kanalni blokdan himoya qiladi)
    description = (
        f"{story['script']}\n\n"
        f"{story['cta']}\n"
        f"Goal: {PART2_LIKE_GOAL} likes for Part 2.\n\n"
        "Abyss Secrets uncovers terrifying deep-sea anomalies, naval encounters, and unmapped trench horrors.\n\n"
        "#Shorts #DeepSeaHorror #AbyssSecrets #OceanMystery"
    )
    tags = ["Shorts", "Deep sea horror", "sea monster", "abyss secrets", "ocean mystery", "submarine disaster"]
    video_id = upload_to_youtube(youtube, story["title"], description, tags, str(final_file))

    history.setdefault("uploaded_ids", []).append(story["id"])
    history.setdefault("video_stats", {})[story["id"]] = {"video_id": video_id, "views": 0, "likes": 0}
    save_history(history)

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "short"
    if mode == "auth":
        get_youtube_service()
        print("✅ OAuth muvaffaqiyatli tayyorlandi.")
    else:
        run_short()
