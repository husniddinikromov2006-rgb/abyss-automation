import os
import sys
import json
import time
import random
import asyncio
import numpy as np
from pathlib import Path

# --- PILLOW MOSLASHTIRISH ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    if hasattr(PIL.Image, 'Resampling'):
        PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
    else:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# ----------------------------

import requests
import edge_tts

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    AudioClip,
    CompositeAudioClip,
)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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

VOICE = "en-US-ChristopherNeural"
MIN_SHORT_SECONDS = 52
LONG_DURATION = 180
LIKE_THRESHOLD_FOR_PART2 = 100

HORROR_ZONES = [
    {"name": "the Mariana Trench Abyssal Graveyard", "depth": "36,000 feet beneath eternal blackness"},
    {"name": "the Devil's Triangle Death Zone", "depth": "26,000 feet of crushing violent pressure"},
    {"name": "Point Nemo Blood Chasm", "depth": "the most isolated nightmare zone on the planet"},
    {"name": "the Antarctic Sub-Glacial Hell Trench", "depth": "sub-zero radioactive black abyssal vents"},
    {"name": "the North Atlantic U-Boat Graveyard", "depth": "18,000 feet beneath freezing war zones"},
    {"name": "the Bikini Atoll Nuclear Crater", "depth": "sunken radioactive military wreckage"}
]

# HARBIY FOJIALAR VA VAHSHIY TITANLAR TO'QNASHUVI
TITAN_BATTLES = [
    {
        "titan_a": "NAZI U-BOAT FLEET WOLFPACK",
        "titan_b": "THE ARMORED CHASM LEVIATHAN",
        "category": "ww2_military_horror",
        "intro": "during World War Two, three German U-boats hunting Allied convoys encountered a bio-luminescent sea titan",
        "violence": "The beast rammed U-boat 480 from beneath, biting the double-steel hull completely in half while deck gunners fired futilely into sixty-foot jaws",
        "aftermath": "leaving shredded torpedo bays and dismembered sailors floating in oil-stained freezing waters",
        "secret": "Recovered Kriegsmarine logbooks recorded that depth charges only infuriated the leviathan, causing it to swallow the second sub whole"
    },
    {
        "titan_a": "COLD WAR SOVIET NUCLEAR SUBMARINE K-129",
        "titan_b": "ANOMALY KRAKEN PRIME",
        "category": "cold_war_carnage",
        "intro": "at the height of the Cold War, a nuclear-armed ballistic submarine vanished after reporting massive acoustic signatures",
        "violence": "Massive barbed tentacles crushed the nuclear reactor compartment, warping the missile silos until seawater detonated the battery banks",
        "aftermath": "leaving the crushed titanium hull strewn across the abyssal trench with hatch locks ripped open from the outside",
        "secret": "Declassified Pentagon surveillance tapes confirmed biological feeding sounds continued around the radioactive wreckage for seven weeks"
    },
    {
        "titan_a": "THE TITANIC BLACK LEVIATHAN",
        "titan_b": "ANOMALY KRAKEN ZERO",
        "category": "titan_war",
        "intro": "a two-hundred-foot armored jaw leviathan collided with a mutated tentacled cephalopod titan",
        "violence": "The leviathan tore three colossal tentacles off, vomiting boiling acidic black bile before Kraken Zero dragged both beasts into a military sub hull",
        "aftermath": "tearing the nuclear sub in two as the ocean boiled with black predator blood and severed limbs",
        "secret": "Hydrophones detected deafening ultrasonic roars as both beasts tore each other apart in total darkness"
    },
    {
        "titan_a": "THE ABYSS SERPENT DEVOURER",
        "titan_b": "PREHISTORIC MEGALODON REX",
        "category": "predator_frenzy",
        "intro": "a serpentine deep-sea demon with six rows of serrated bone fangs ambushed a seventy-foot apex mega-predator",
        "violence": "The Devourer clamped its translucent venom fangs around the monster's spine, violently shaking until the ribcage collapsed into red mist",
        "aftermath": "leaving shredded biological flesh and massive bite-marks glowing with deep toxic bio-radiation",
        "secret": "Naval satellites recorded thermal spikes equivalent to an underwater blast as the predators slaughtered each other"
    },
    {
        "titan_a": "OPERATION HIGHJUMP SECRET NAVAL FLEET",
        "titan_b": "THE ANTARCTIC CHASM PHANTOMS",
        "category": "military_slaughter",
        "intro": "a heavily armed naval task force in Antarctica probed deep sub-glacial hydrothermal trenches",
        "violence": "Bio-luminescent winged predators breached the ice shelf, dragging destroyers into the freezing vortex while shredding steel armor plates",
        "aftermath": "leaving burning wreckage and zero bodies recovered across the frozen continental shelf",
        "secret": "Naval commanders ordered surviving radar tapes immediately classified under executive military treason laws"
    }
]

# FAQAT ENG DAHSHATLI, HARBIY VA TISHLAR BILAN TO'LA QIDIRUVLAR
HORROR_QUERY_POOLS = [
    [
        "scary monster underwater dark horror teeth",
        "submarine emergency alarm red flashing dark",
        "underwater warship explosion dark ocean",
        "giant sea monster attack dark waters",
        "underwater wreckage dark trench horror"
    ],
    [
        "terrifying deep sea predator jaws attacking",
        "giant squid kraken destroying ship ocean horror",
        "underwater dark red blood horror scary",
        "naval submarine sinking emergency dark horror",
        "sonar display dark red panic emergency"
    ],
    [
        "scary ocean leviathan silhouette dark cinematic",
        "creature stalking submarine dark lights horror",
        "storm waves dark ocean destruction night scary",
        "deep sea monster fighting underwater horror",
        "underwater panic flashing red siren horror"
    ]
]

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {"uploaded_ids": [], "video_stats": {}, "pending_part2": [], "favorite_category": "ww2_military_horror"}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("uploaded_ids", [])
        data.setdefault("video_stats", {})
        data.setdefault("pending_part2", [])
        data.setdefault("favorite_category", "ww2_military_horror")
        return data
    except Exception:
        return {"uploaded_ids": [], "video_stats": {}, "pending_part2": [], "favorite_category": "ww2_military_horror"}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def get_youtube_service():
    token_data = os.environ.get("YOUTUBE_TOKEN_JSON")
    if token_data:
        creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        raise FileNotFoundError("token.json yoki YOUTUBE_TOKEN_JSON topilmadi.")

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("youtube", "v3", credentials=creds)

def sync_and_analyze_stats(youtube, history):
    pending = history.get("pending_part2", [])
    if pending:
        video_ids = [item["video_id"] for item in pending]
        try:
            req = youtube.videos().list(part="statistics", id=",".join(video_ids[:50]))
            res = req.execute()
            stats_map = {}
            for item in res.get("items", []):
                stats_map[item["id"]] = {
                    "likes": int(item["statistics"].get("likeCount", 0)),
                    "views": int(item["statistics"].get("viewCount", 0))
                }

            for entry in history["pending_part2"]:
                vid = entry["video_id"]
                if vid in stats_map:
                    entry["likes"] = stats_map[vid]["likes"]
                    entry["views"] = stats_map[vid]["views"]
        except Exception as e:
            print(f"⚠️ Statistika tahlili: {e}")

    categories = {"ww2_military_horror": 0, "cold_war_carnage": 0, "titan_war": 0, "predator_frenzy": 0, "military_slaughter": 0}
    for item in pending:
        cat = item.get("category", "ww2_military_horror")
        categories[cat] = categories.get(cat, 0) + item.get("views", 0)

    best_cat = max(categories, key=categories.get)
    history["favorite_category"] = best_cat
    print(f"🩸 Tomoshabinlar eng ko'p vahima bilan tomosha qilgan yo'nalish: {best_cat.upper()}")
    return history

def pick_next_story(history):
    pending = history.get("pending_part2", [])
    ready_for_part2 = [p for p in pending if p.get("likes", 0) >= LIKE_THRESHOLD_FOR_PART2]

    # 100 ta layk to'plangan bo'lsa, Part 2 fojiasi chiqadi
    if ready_for_part2:
        chosen = ready_for_part2[0]
        history["pending_part2"].remove(chosen)
        z = chosen["zone"]
        b = chosen["battle"]
        year = chosen["year"]
        story_id = f"military_carnage_{year}_part2".lower()

        title = f"DEEP WAR MASSACRE: What Slagged The Fleet (Part 2) ☠️🔥 #Shorts"
        script = (
            f"You smashed 100 likes on Part 1. Here is the unredacted military slaughter log. "
            f"When naval recovery divers reached the wreckage inside {z['name']}, the hull was liquefied from the outside. "
            f"{b['aftermath']}. {b['secret']}. "
            f"These ancient horrors used naval warfare explosions as a feeding signal. Never cross these waters at night."
        )
        return {
            "id": story_id,
            "title": title,
            "script": script,
            "queries": random.choice(HORROR_QUERY_POOLS),
            "cta": "Subscribe to Abyss Secrets for full declassified military horrors.",
            "is_part2": True,
            "is_standalone": False
        }

    fav_cat = history.get("favorite_category", "ww2_military_horror")
    matching = [b for b in TITAN_BATTLES if b["category"] == fav_cat]
    battle = random.choice(matching) if matching else random.choice(TITAN_BATTLES)

    zone = random.choice(HORROR_ZONES)
    # Tarixiy urushlar yillari (WW2 dan tortib Sovuq urush va hozirgacha)
    year = random.choice([1942, 1944, 1956, 1968, 1974, 1986, 1991, 2003, 2018])

    is_standalone = random.choice([True, False])

    if is_standalone:
        # Bitta qismda tugaydigan qora harbiy voqea
        story_id = f"military_slaughter_{year}_{random.randint(100, 999)}"
        title = f"WAR ARCHIVE {year}: {battle['titan_a']} vs {battle['titan_b']} 🚨☠️ #Shorts"
        script = (
            f"Top secret naval disaster log. In {year}, deep beneath {zone['name']}, classified warfare triggered a nightmare. "
            f"Without warning, {battle['intro']}. "
            f"{battle['violence']}! "
            f"{battle['secret']}. "
            f"The military covered up the incident, logging the catastrophe as a boiler malfunction. But the wreckage speaks the truth."
        )
        cta = "Subscribe immediately to unlock unredacted naval massacre archives."
        return {
            "id": story_id,
            "title": title,
            "script": script,
            "queries": random.choice(HORROR_QUERY_POOLS),
            "cta": cta,
            "is_part2": False,
            "is_standalone": True
        }
    else:
        # Part 1 zanjiri
        story_id = f"war_clash_{year}_part1"
        title = f"DECLASSIFIED {year}: {battle['titan_a']} Encounter (Part 1) 🚨🩸 #Shorts"
        script = (
            f"Do not watch this in the dark. In {year}, inside {zone['name']}, "
            f"sonar crews went into total hysteria as {battle['intro']}. "
            f"Spotlights captured pure slaughter: {battle['violence']}! "
            f"Bulkheads buckled like paper under five hundred tons of raw monstrous force."
        )
        cta = "Smash 100 likes right now if you want Part 2: the recovered black-box distress tape."
        return {
            "id": story_id,
            "title": title,
            "script": script,
            "queries": random.choice(HORROR_QUERY_POOLS),
            "cta": cta,
            "is_part2": False,
            "is_standalone": False,
            "metadata_bundle": {
                "zone": zone,
                "battle": battle,
                "year": year,
                "category": battle["category"]
            }
        }

def generate_long_form_story():
    """Haftasiga 2 marta chiqadigan 3 daqiqalik yirik harbiy maxluqlar to'qnashuvi."""
    zone = random.choice(HORROR_ZONES)
    b1 = random.choice(TITAN_BATTLES)
    b2 = random.choice(TITAN_BATTLES)

    title = f"CLASSIFIED: The Secret Naval Slaughter in the Mariana Trench (Full 3-Minute Tape) 🚨☠️"
    script = (
        f"Warning: The following audio-visual logs are classified Top Secret under maritime warfare protocols. "
        f"For over fifty years, world superpowers buried the slaughter that took place in {zone['name']}. "
        f"During classified naval operations, reconnaissance hydrophones recorded {b1['intro']}. "
        f"The ocean became an underwater slaughterhouse as {b1['violence']}. "
        f"Within forty minutes, secondary emergency alarms blared across the fleet: {b2['intro']}. "
        f"The entities collided in an orgy of bone-shattering violence: {b2['violence']}! "
        f"Entire naval battle groups were obliterated from beneath, dragged past crushing depth. "
        f"{b1['secret']}, while {b2['secret']}. "
        f"The abyss is armed with predators far deadlier than nuclear arsenals. "
        f"Subscribe to Abyss Secrets before these unredacted war tapes are deleted forever."
    )
    queries = [
        "scary monster underwater dark horror teeth",
        "submarine emergency alarm red flashing dark",
        "underwater warship explosion dark ocean",
        "giant monster jaws underwater terrifying",
        "naval submarine sinking emergency dark horror",
        "underwater dark red blood horror scary",
        "deep sea monster fighting underwater horror"
    ]
    return {
        "id": f"long_naval_carnage_{int(time.time())}",
        "title": title,
        "script": script,
        "queries": queries,
        "is_long": True
    }

async def generate_voice(text, filename):
    rates = ["+2%", "+3%"]
    pitches = ["-3Hz", "-4Hz"]
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
        heartbeat = np.sin(2 * np.pi * 50.0 * t) * np.maximum(0, np.sin(2 * np.pi * 1.45 * t)) ** 8 * 0.50
        drone = np.sin(2 * np.pi * 36.0 * t) * 0.30 + np.sin(2 * np.pi * 55.0 * t) * 0.22
        screech = np.sin(2 * np.pi * 135.0 * t + np.sin(2 * np.pi * 3.0 * t)) * 0.12
        alarm = np.sin(2 * np.pi * 440.0 * t) * np.maximum(0, np.sin(2 * np.pi * 1.0 * t)) ** 12 * 0.15
        audio = (heartbeat + drone + screech + alarm) * 0.28
        return np.vstack((audio, audio)).T
    return AudioClip(make_frame, duration=duration, fps=sample_rate)

def search_pexels(query, per_page=15):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    for _ in range(3):
        try:
            r = requests.get(url, headers=headers, params={"query": query, "per_page": per_page}, timeout=30)
            r.raise_for_status()
            return r.json().get("videos", [])
        except Exception:
            time.sleep(2)
    return []

def download_one_pexels(query, output_file, is_portrait=True):
    max_retries = 4
    for attempt in range(max_retries):
        try:
            videos = search_pexels(query)
            if not videos:
                videos = search_pexels("scary monster underwater dark horror")
            if not videos:
                time.sleep(2)
                continue

            random.shuffle(videos)
            video = videos[0]
            files = video.get("video_files", [])

            if is_portrait:
                matching = [f for f in files if f.get("height", 0) > f.get("width", 0)]
            else:
                matching = [f for f in files if f.get("width", 0) >= f.get("height", 0)]

            selected = max(matching, key=lambda x: x.get("width", 0)) if matching else max(files, key=lambda x: x.get("width", 0))
            link = selected["link"]

            with requests.get(link, stream=True, timeout=60) as resp:
                resp.raise_for_status()
                with open(str(output_file), "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

            if os.path.exists(output_file) and os.path.getsize(output_file) > 10000:
                return
        except Exception as e:
            print(f"⚠️ Qayta urinish ({attempt + 1}/{max_retries}): {e}")
            time.sleep(3)

    raise ConnectionError("Video yuklab olinmadi.")

def crop_video(clip, target_w, target_h):
    w, h = clip.size
    target_ratio = target_w / target_h
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        x1 = int((w - new_w) / 2)
        clip = clip.crop(x1=x1, y1=0, x2=x1 + new_w, y2=h)
    else:
        new_h = int(w / target_ratio)
        y1 = int((h - new_h) / 2)
        clip = clip.crop(x1=0, y1=y1, x2=w, y2=y1 + new_h)

    return clip.resize((target_w, target_h))

def render_movie(story, voice_file, output_file, is_long=False):
    target_w, target_h = (1920, 1080) if is_long else (1080, 1920)
    voice_audio = AudioFileClip(str(voice_file))
    total_duration = LONG_DURATION if is_long else max(voice_audio.duration, MIN_SHORT_SECONDS)

    horror_audio = make_horror_soundscape(total_duration)
    final_audio = CompositeAudioClip([voice_audio, horror_audio])

    queries = story["queries"]
    scene_count = len(queries)
    scene_duration = total_duration / scene_count

    clips = []
    temp_files = []

    try:
        for i in range(scene_count):
            query = queries[i]
            raw_file = OUT_DIR / f"scene_{story['id']}_{i}.mp4"
            temp_files.append(raw_file)
            print(f"🩸 Harbiy Vahshat Sahna {i + 1}/{scene_count}: {query}")

            download_one_pexels(query, str(raw_file), is_portrait=not is_long)
            clip = VideoFileClip(str(raw_file))
            clip = crop_video(clip, target_w, target_h)

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
            fps=24,
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
    res = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    vid = res["id"]
    print(f"🚀 YUKLANDI: https://youtu.be/{vid}")
    return vid

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "short"
    youtube = get_youtube_service()
    history = load_history()

    history = sync_and_analyze_stats(youtube, history)

    if mode == "long":
        story = generate_long_form_story()
        is_long = True
        narration = story["script"]
    else:
        story = pick_next_story(history)
        is_long = False
        narration = story["script"] + " " + story["cta"]

    print(f"\n⚠️ ISHGA TUSHDI: {story['title']}")

    voice_file = OUT_DIR / f"{story['id']}_voice.mp3"
    final_file = OUT_DIR / f"{story['id']}_video.mp4"

    asyncio.run(generate_voice(narration, str(voice_file)))
    render_movie(story, voice_file, final_file, is_long=is_long)

    desc = (
        f"{story['script']}\n\n"
        "Abyss Secrets uncovers classified naval horrors, WW2 submarine massacres, and deep trench monster wars.\n\n"
        "#DeepSeaHorror #AbyssSecrets #WW2Mystery #ColdWarHorror #Leviathan #Shorts"
    )
    tags = ["Deep sea horror", "naval massacre", "submarine disaster", "abyss secrets", "ww2 monster encounter", "kraken attack"]
    video_id = upload_to_youtube(youtube, story["title"], desc, tags, final_file)

    history.setdefault("uploaded_ids", []).append(story["id"])
    if not is_long and not story.get("is_part2") and not story.get("is_standalone"):
        bundle = story.get("metadata_bundle", {})
        history["pending_part2"].append({
            "video_id": video_id,
            "likes": 0,
            "views": 0,
            "category": bundle.get("category", "ww2_military_horror"),
            "zone": bundle.get("zone"),
            "battle": bundle.get("battle"),
            "year": bundle.get("year")
        })

    save_history(history)

if __name__ == "__main__":
    main()
