import os
import glob
import requests
import subprocess
from story_brain import get_daily_content_plan

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
VIDEOS_DIR = "videos"
OUTPUT_DIR = "output"
MUSIC_DIR = "music"

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

def download_footage(queries):
    headers = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else {}
    downloaded = []
    print("\n--- 1. Pexels'dan 4K kadrlar olinmoqda ---")

    for idx, query in enumerate(queries):
        file_path = os.path.join(VIDEOS_DIR, f"clip_{idx}.mp4")
        if not PEXELS_API_KEY:
            print("[XATO]: PEXELS_API_KEY topilmadi!")
            continue

        try:
            url = f"[https://api.pexels.com/videos/search?query=](https://api.pexels.com/videos/search?query=){query}&per_page=5&orientation=landscape"
            r = requests.get(url, headers=headers, timeout=20).json()
            videos = r.get("videos", [])

            if not videos:
                clean_term = query.split()[0] + " nature 4k"
                url_alt = f"[https://api.pexels.com/videos/search?query=](https://api.pexels.com/videos/search?query=){clean_term}&per_page=3"
                r = requests.get(url_alt, headers=headers, timeout=20).json()
                videos = r.get("videos", [])

            if videos:
                files = videos[0].get("video_files", [])
                best = max(files, key=lambda x: (x.get("width", 0), x.get("height", 0)))
                link = best.get("link")

                resp = requests.get(link, stream=True, timeout=60)
                with open(file_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

                downloaded.append(file_path)
                print(f"[YUKLANDI]: {query}")
        except Exception as e:
            print(f"[XATO]: {query} yuklanmadi: {e}")

    return downloaded

def resolve_audio():
    tracks = glob.glob(os.path.join(MUSIC_DIR, "*.mp3"))
    if tracks:
        return tracks[0]

    # Musiqa topilmasa xatolik bermasdan sokin fon audiosi yaratadi
    silent_audio = os.path.join(MUSIC_DIR, "ambient_silence.mp3")
    if not os.path.exists(silent_audio):
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", "130", "-q:a", "9", "-acodec", "libmp3lame", silent_audio
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return silent_audio

def render_long_form(clips, audio, country):
    print("\n--- 2. 2 Daqiqalik Asosiy Video Render qilinmoqda (16:9) ---")
    safe_name = country.replace(" ", "_")
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name}_Cinematic_2Min.mp4")
    concat_txt = "concat_main.txt"

    # Har biri 5 soniyadan iborat 24 ta kadr = 120 soniya (2 daqiqa)
    extended = (clips * 10)[:24]
    with open(concat_txt, "w") as f:
        for c in extended:
            f.write(f"file '{os.path.abspath(c)}'\n")
            f.write("duration 5\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", audio, "-t", "120",
        "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
        "-af", "afade=t=out:st=117:d=3",
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(concat_txt):
        os.remove(concat_txt)
    print(f"[TAYYOR]: {output_path}")

def render_shorts(clips, audio, country):
    print("\n--- 3. AQSH auditoriyasi uchun 4 ta Shorts yasalmoqda (9:16) ---")
    safe_name = country.replace(" ", "_")

    for i in range(4):
        short_path = os.path.join(OUTPUT_DIR, f"{safe_name}_Short_{i+1}.mp4")
        concat_short = f"concat_short_{i}.txt"

        offset = i * 2
        short_clips = (clips[offset:] + clips[:offset])[:6]
        with open(concat_short, "w") as f:
            for c in short_clips:
                f.write(f"file '{os.path.abspath(c)}'\n")
                f.write("duration 5\n")

        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_short,
            "-i", audio, "-t", "30",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-af", "afade=t=out:st=28:d=2",
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            short_path
        ]
        subprocess.run(cmd, check=True)
        if os.path.exists(concat_short):
            os.remove(concat_short)
        print(f"[TAYYOR SHORT {i+1}]: {short_path}")

if __name__ == "__main__":
    plan = get_daily_content_plan()
    country = plan.get("country", "Earth")
    print(f"\nTanlangan joy: {country} | {plan.get('theme', '')}")

    clips = download_footage(plan.get("queries", []))
    if clips:
        audio = resolve_audio()
        render_long_form(clips, audio, country)
        render_shorts(clips, audio, country)
        print("\n=== 1 TA ASOSIY 2 DAQIQALIK VIDEO VA 4 TA SHORTS TO'LIQ BITDI ===")
    else:
        print("[XATO]: Kadrlar yuklanmadi. PEXELS_API_KEY to'g'riligini tekshiring.")
