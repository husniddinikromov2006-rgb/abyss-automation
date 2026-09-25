import os
import sys
import json
import time
import random
import asyncio
import argparse
import urllib.parse
import shutil
from pathlib import Path
import requests

import PIL.Image
from PIL import ImageDraw, ImageFont
if not hasattr(PIL.Image, 'ANTIALIAS'):
    if hasattr(PIL.Image, 'Resampling'):
        PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
    else:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import numpy as np
import edge_tts
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    AudioClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ColorClip
)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from story_brain import get_unique_story

SCOPES = [
    "https://www.googleapis.com/auth/youtube"
]

HISTORY_FILE = "history.json"
OUT_DIR = Path("media_workspace")
OUT_DIR.mkdir(exist_ok=True)
VOICE = "en-US-ChristopherNeural"

def get_youtube_service():
    token_data = os.environ.get("YOUTUBE_TOKEN_JSON")
    if token_data:
        creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        raise FileNotFoundError("YOUTUBE_TOKEN_JSON topilmadi.")

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("youtube", "v3", credentials=creds)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {
            "uploaded_videos": [],
            "past_titles": [],
            "past_hooks": [],
            "best_theme": "sunken nuclear submarine breach",
            "series_episode": 1
        }
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("uploaded_videos", [])
        data.setdefault("past_titles", [])
        data.setdefault("past_hooks", [])
        data.setdefault("best_theme", "sunken nuclear submarine breach")
        data.setdefault("series_episode", 1)
        return data
    except Exception:
        return {
            "uploaded_videos": [],
            "past_titles": [],
            "past_hooks": [],
            "best_theme": "sunken nuclear submarine breach",
            "series_episode": 1
        }

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def analyze_channel_performance(youtube, history):
    try:
        req = youtube.channels().list(part="contentDetails", mine=True)
        res = req.execute()
        uploads_playlist = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        pl_req = youtube.playlistItems().list(part="snippet", playlistId=uploads_playlist, maxResults=15)
        pl_res = pl_req.execute()
        video_ids = [item["snippet"]["resourceId"]["videoId"] for item in pl_res.get("items", [])]

        if not video_ids:
            return history

        v_req = youtube.videos().list(part="snippet,statistics", id=",".join(video_ids))
        v_res = v_req.execute()

        best_score = -1
        winning_title = ""

        for item in v_res.get("items", []):
            stats = item.get("statistics", {})
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            score = views + (likes * 10)
            title = item.get("snippet", {}).get("title", "")

            if title and title not in history["past_titles"]:
                history["past_titles"].append(title)

            if score > best_score:
                best_score = score
                winning_title = title

        if winning_title:
            history["best_theme"] = f"Audience engagement theme: {winning_title}"
            print(f"📊 KANAL TAHLILI: Eng yuqori ko'rsatkich -> {winning_title} (Ball: {best_score})")

    except Exception as e:
        print(f"⚠️ Kanal tahlili ogohlantirishi: {e}")

    return history

def download_ai_image(prompt, out_path, width, height):
    encoded = urllib.parse.quote(prompt)
    seed = random.randint(1000, 999999)
    url_flux = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&model=flux&nologo=true"
    url_turbo = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&model=turbo&nologo=true"

    for url in [url_flux, url_turbo]:
        for _ in range(2):
            try:
                r = requests.get(url, timeout=35)
                if r.status_code == 200 and len(r.content) > 15000:
                    with open(str(out_path), "wb") as f:
                        f.write(r.content)
                    return True
            except Exception:
                time.sleep(1.5)
    return False

def make_horror_soundscape(duration):
    sample_rate = 44100
    def make_frame(t):
        heartbeat = np.sin(2 * np.pi * 55.0 * t) * np.maximum(0, np.sin(2 * np.pi * 1.5 * t)) ** 8 * 0.55
        drone = np.sin(2 * np.pi * 40.0 * t) * 0.35 + np.sin(2 * np.pi * 60.0 * t) * 0.25
        screech = np.sin(2 * np.pi * 140.0 * t + np.sin(2 * np.pi * 3.5 * t)) * 0.15
        alarm = np.sin(2 * np.pi * 440.0 * t) * np.maximum(0, np.sin(2 * np.pi * 1.2 * t)) ** 14 * 0.22
        audio = (heartbeat + drone + screech + alarm) * 0.30
        return np.vstack((audio, audio)).T
    return AudioClip(make_frame, duration=duration, fps=sample_rate)

async def generate_voice(text, filename):
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate="+3%", pitch="-2Hz")
    await communicate.save(str(filename))

def create_cinematic_clip(image_path, duration, target_w, target_h):
    clip = ImageClip(str(image_path)).set_duration(duration)
    img_w, img_h = clip.size
    target_ratio = target_w / target_h
    current_ratio = img_w / img_h

    if current_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        clip = clip.crop(x1=int((img_w - new_w) / 2), y1=0, x2=int((img_w + new_w) / 2), y2=img_h)
    else:
        new_h = int(img_w / target_ratio)
        clip = clip.crop(x1=0, y1=int((img_h - new_h) / 2), x2=img_w, y2=int((img_h + new_h) / 2))

    clip = clip.resize((target_w, target_h))
    zoomed = clip.resize(lambda t: 1.0 + 0.07 * (t / duration))
    return zoomed.set_duration(duration)

def create_subtitle_clips(scenes, target_w, target_h, is_horizontal=False):
    sub_clips = []
    temp_imgs = []
    y_pos = int(target_h * 0.85) if is_horizontal else int(target_h * 0.75)
    font_size = int(target_w * 0.035) if is_horizontal else int(target_w * 0.052)
    max_line_len = 45 if is_horizontal else 22

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    cur_time = 0.0
    for i, sc in enumerate(scenes):
        dur = sc["duration"]
        text = sc.get("text", "")
        if not text:
            cur_time += dur
            continue

        img = PIL.Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        words = text.split()
        lines = []
        cur_l = []
        for w in words:
            cur_l.append(w)
            if len(" ".join(cur_l)) > max_line_len:
                lines.append(" ".join(cur_l))
                cur_l = []
        if cur_l:
            lines.append(" ".join(cur_l))
        display_text = "\n".join(lines[:2])

        for ox, oy in [(-3,-3), (3,-3), (-3,3), (3,3), (-3,0), (3,0), (0,-3), (0,3)]:
            draw.text((target_w // 2 + ox, y_pos + oy), display_text, font=font, fill=(0, 0, 0, 255), anchor="mm", align="center")
        draw.text((target_w // 2, y_pos), display_text, font=font, fill=(255, 235, 59, 255), anchor="mm", align="center")

        path = OUT_DIR / f"sub_{i}_{int(time.time()*1000)}.png"
        img.save(str(path))
        temp_imgs.append(path)

        clip = ImageClip(str(path)).set_start(cur_time).set_duration(dur)
        sub_clips.append(clip)
        cur_time += dur

    return sub_clips, temp_imgs

def render_dynamic_movie(scenes, voice_file, output_file, total_duration, target_w, target_h, is_horizontal=False):
    voice_audio = AudioFileClip(str(voice_file))
    horror_audio = make_horror_soundscape(total_duration)
    final_audio = CompositeAudioClip([voice_audio, horror_audio]).subclip(0, total_duration)

    clips = []
    temp_files = []

    try:
        for i, sc in enumerate(scenes):
            img_path = OUT_DIR / f"frame_{i}.jpg"
            temp_files.append(img_path)
            print(f"🎬 Kadr tayyorlanmoqda ({i+1}/{len(scenes)})...")
            download_ai_image(sc["prompt"], img_path, target_w, target_h)
            clip = create_cinematic_clip(img_path, sc["duration"], target_w, target_h)
            clips.append(clip)

        base_video = concatenate_videoclips(clips, method="compose").subclip(0, total_duration)
        red_flash = ColorClip(size=(target_w, target_h), color=[255, 0, 0]).set_duration(0.18).set_opacity(0.35)
        sub_clips, sub_imgs = create_subtitle_clips(scenes, target_w, target_h, is_horizontal)
        temp_files.extend(sub_imgs)

        all_layers = [base_video, red_flash.set_start(2.5)] + sub_clips
        final_video = CompositeVideoClip(all_layers).set_duration(total_duration).set_audio(final_audio)

        final_video.write_videofile(
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
        final_video.close()
        for c in clips:
            c.close()
    finally:
        for f in temp_files:
            try:
                if f.exists():
                    f.unlink()
            except Exception:
                pass

def post_community_update(youtube, story):
    text = story.get("text", "Declassified expedition log update...")
    print(f"\n📢 COMMUNITY POST YARATILDI:\n{text}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["shorts", "long_3min", "series_4min", "post"], default="shorts")
    args = parser.parse_args()

    youtube = get_youtube_service()
    history = load_history()

    # 1. Kanal tahlili
    history = analyze_channel_performance(youtube, history)

    # 2. Rejim parametrlari
    is_horizontal = args.mode in ["long_3min", "series_4min"]
    target_w, target_h = (1920, 1080) if is_horizontal else (1080, 1920)
    current_episode = history.get("series_episode", 1)

    # 3. Syujetni olish
    story = get_unique_story(
        winning_theme=history.get("best_theme", "deep sea military disaster"),
        past_titles=history.get("past_titles", []),
        past_hooks=history.get("past_hooks", []),
        mode=args.mode,
        episode_num=current_episode
    )

    if args.mode == "post":
        post_community_update(youtube, story)
        return

    title = story.get("title", "CLASSIFIED NAVAL LOG")
    if args.mode == "shorts" and "#Shorts" not in title:
        title += " #Shorts"

    script = story.get("script", "")
    hook = story.get("hook", "")
    scenes = story.get("scenes", [])

    print(f"\n⚡ YARATILAYOTGAN FORMAT: {args.mode.upper()}")
    print(f"🎬 Video nomi: {title}")
    print(f"🎯 Hook (0-3s): \"{hook}\"")

    voice_path = OUT_DIR / f"{int(time.time())}_voice.mp3"
    video_path = OUT_DIR / f"{int(time.time())}_final.mp4"

    asyncio.run(generate_voice(script, str(voice_path)))
    voice_clip = AudioFileClip(str(voice_path))

    min_dur = 240.0 if args.mode == "series_4min" else (180.0 if args.mode == "long_3min" else 55.0)
    total_dur = max(min_dur, voice_clip.duration)
    voice_clip.close()

    scene_dur = total_dur / len(scenes)
    for sc in scenes:
        sc["duration"] = scene_dur

    render_dynamic_movie(scenes, voice_path, video_path, total_dur, target_w, target_h, is_horizontal)

    desc = f"{script}\n\n#DeepSeaHorror #NavalHorror #AbyssSecrets #Declassified #OceanMystery #Documentary"
    tags = ["Deep sea horror", "US Navy horror", "submarine disaster", "ocean mystery", "abyss documentary", "classified logs"]

    body = {
        "snippet": {"title": title, "description": desc, "tags": tags, "categoryId": "28"},
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    res = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    vid = res["id"]
    print(f"🚀 VIDEO MUVAFFAQIYATLI YUKLANDI: https://youtu.be/{vid}")

    # Xotirani yangilash
    history["uploaded_videos"].append(vid)
    history["past_titles"].append(title)
    if hook:
        history["past_hooks"].append(hook)
    if args.mode == "series_4min":
        history["series_episode"] = current_episode + 1
    save_history(history)

    try:
        shutil.rmtree(str(OUT_DIR))
        OUT_DIR.mkdir(exist_ok=True)
    except Exception:
        pass

if __name__ == "__main__":
    main()
