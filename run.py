import os
import glob
import datetime
import requests
import subprocess
from story_brain import get_daily_content_plan

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
TARGET_MODE = os.getenv("TARGET_MODE", "").strip().lower()

VIDEOS_DIR = "videos"
OUTPUT_DIR = "output"
MUSIC_DIR = "music"

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

def get_current_task():
    if TARGET_MODE:
        return TARGET_MODE
    utc_hour = datetime.datetime.now(datetime.timezone.utc).hour
    if utc_hour == 1:
        return "main"
    elif utc_hour == 6:
        return "short1"
    elif utc_hour == 11:
        return "short2"
    elif utc_hour == 15:
        return "short3"
    elif utc_hour == 19:
        return "short4"
    return "all"

def download_footage(queries):
    headers = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else {}
    downloaded = []
    print("\n--- Pexels'dan 4K kadrlar olinmoqda ---")
    for idx, query in enumerate(queries):
        file_path = os.path.join(VIDEOS_DIR, f"clip_{idx}.mp4")
        if not PEXELS_API_KEY:
            continue
        try:
            url = f"https://api.pexels.com/videos/search?query={query}&per_page=5&orientation=landscape"
            r = requests.get(url, headers=headers, timeout=20).json()
            videos = r.get("videos", [])
            if not videos:
                clean_term = query.split()[0] + " nature landscape 4k"
                url_alt = f"https://api.pexels.com/videos/search?query={clean_term}&per_page=3"
                r = requests.get(url_alt, headers=headers, timeout=20).json()
                videos = r.get("videos", [])

            if videos:
                files = videos[0].get("video_files", [])
                best = max(files, key=lambda x: (x.get("width", 0), x.get("height", 0)))
                link = best.get("link")
                resp = requests.get(link, stream=True, timeout=60)
                with open(file_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        if chunk: f.write(chunk)
                downloaded.append(file_path)
                print(f"[YUKLANDI]: {query}")
        except Exception as e:
            print(f"[XATO]: {query}: {e}")
    return downloaded

def resolve_audio():
    tracks = glob.glob(os.path.join(MUSIC_DIR, "*.mp3"))
    if tracks:
        return tracks[0]
    silent_audio = os.path.join(MUSIC_DIR, "ambient_silence.mp3")
    if not os.path.exists(silent_audio):
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", "130", "-q:a", "9", "-acodec", "libmp3lame", silent_audio
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return silent_audio

def render_main_video(clips, audio, country):
    print("\n--- 2 Daqiqalik Asosiy Video Render qilinmoqda ---")
    safe_name = country.replace(" ", "_")
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name}_Main_2Min.mp4")
    concat_txt = "concat_main.txt"
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
    if os.path.exists(concat_txt): os.remove(concat_txt)
    print(f"[TAYYOR]: {output_path}")

def render_single_short(clips, audio, country, short_index):
    print(f"\n--- Shorts #{short_index} Render qilinmoqda ---")
    safe_name = country.replace(" ", "_")
    short_path = os.path.join(OUTPUT_DIR, f"{safe_name}_Short_{short_index}.mp4")
    concat_short = f"concat_short_{short_index}.txt"

    offset = (short_index - 1) * 2
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
    if os.path.exists(concat_short): os.remove(concat_short)
    print(f"[TAYYOR]: {short_path}")

if __name__ == "__main__":
    task = get_current_task()
    print(f"Joriy reja vazifasi: {task.upper()}")

    plan = get_daily_content_plan()
    country = plan.get("country", "Earth")
    clips = download_footage(plan.get("queries", []))

    if clips:
        audio = resolve_audio()
        if task == "main":
            render_main_video(clips, audio, country)
        elif task == "short1":
            render_single_short(clips, audio, country, 1)
        elif task == "short2":
            render_single_short(clips, audio, country, 2)
        elif task == "short3":
            render_single_short(clips, audio, country, 3)
        elif task == "short4":
            render_single_short(clips, audio, country, 4)
        else: # "all" holatida hammasini birvarakayiga yasaydi
            render_main_video(clips, audio, country)
            for i in range(1, 5):
                render_single_short(clips, audio, country, i)
        print("\n=== VAZIFA MUVAFFAQIYATLI YAKUNLANDI ===")
    else:
        print("[XATO]: Kadrlar yuklanmadi. Kalitni tekshiring.")
