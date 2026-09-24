import os
import json
import random
import sys
import asyncio
from zoneinfo import ZoneInfo
import requests
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ==================== SOZLAMALAR VA KALITLAR ====================
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "EdoUks31ZIxOOLAE35gYGpgiP3ikgDFZBiTlmDEievg9OUnR87AGxoLX")
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]
HISTORY_FILE = "history.json"
US_TIMEZONE = ZoneInfo("America/New_York")

# ==================== YUQORI RETENTION & ENGAGEMENT SSENARIYLARI ====================
SHORTS_STORIES = [
    {
        "id": "creature_challenger_crushed",
        "category": "creature",
        "series": "Mariana Anomaly",
        "part": 1,
        "min_likes": 500,
        "title": "It Severed a Solid Titanium Submarine at 36,000 Feet ⚠️ #Shorts #AbyssSecrets",
        "text": "Do not watch this alone in the dark. In 2011, an autonomous research drone sank past thirty-two thousand feet into the Mariana Trench. Suddenly, its acoustic telemetry detected a colossal biological entity measuring over eighty meters, circling the vessel. Within seconds, exterior microphones logged a deafening sub-bass frequency, followed by the sickening sound of three-inch reinforced titanium snapping like a twig. When surface vessels retrieved the snapped tether, the forward titanium cabin was completely gone, bearing massive serrated bite marks dripping with unknown bioluminescent enzymes. Marine acoustic labs confirmed no known living animal could exert that bite force at that depth. Did they disturb a prehistoric leviathan? Once this video reaches 500 likes, I will play the unedited black box audio frequency in Part 2. Hit subscribe and drop your theory in the comments right now.",
        "query": "deep sea dark underwater trench monster scary ocean"
    },
    {
        "id": "cia_gateway_astral",
        "category": "declassified",
        "series": "Project Gateway",
        "part": 1,
        "min_likes": 500,
        "title": "Declassified CIA File Confirms Human Soul Can Leave Body ⚠️ #Shorts #SecretFiles",
        "text": "This is official CIA document CIA-RDP96-00788R001700210016-5. In 1983, the Central Intelligence Agency and US Army Intelligence compiled an extensive scientific study titled Analysis and Assessment of Gateway Process. The document officially confirms that human consciousness is not biological, but a localized energy matrix capable of projecting beyond space and time. Using synchronized hemispheric brainwave frequencies, test subjects separated their consciousness from their physical bodies, traveling through solid walls and accurately reporting classified Soviet coordinates in real time. Page twenty-five was confiscated and kept classified by the Department of Defense for forty years. If this video reaches 500 likes, we decode the missing page twenty-five. Subscribe to Abyss Secrets right now so you do not miss it, and tell me: have you ever experienced an astral projection?",
        "query": "secret documents classified room glowing vintage laboratory"
    },
    {
        "id": "creature_point_nemo_nest",
        "category": "creature",
        "series": "Point Nemo",
        "part": 1,
        "min_likes": 500,
        "title": "Satellite Images Captured Massive Movement at Point Nemo 🌊 #Shorts #OceanHorror",
        "text": "Point Nemo is the most isolated location on planet Earth, where the closest humans are astronauts aboard the International Space Station. In late 2022, military satellites detected an inexplicable thermal anomaly spreading across forty square miles of open ocean. Naval hydrophone arrays simultaneously recorded ultra-low frequency biological rhythms echoing from two miles beneath the seafloor. Even more terrifying, deep-sea research buoys deployed in the sector suddenly went silent one after another, their reinforced cables cleanly severed from below. Marine biologists cannot explain what organic organism could generate that much heat in freezing oceanic abysses. Drop your honest thoughts in the comments. When we hit 500 likes, Part 2 drops with the recovered sonar waveforms. Hit that subscribe button now.",
        "query": "stormy dark ocean waves giant whirlpool deep underwater"
    },
    {
        "id": "pentagon_northwoods_terror",
        "category": "declassified",
        "series": "Operation Northwoods",
        "part": 0,
        "min_likes": 0,
        "title": "Declassified: The Pentagon's Dark False Flag Plot ⚠️ #Shorts #HistoryMystery",
        "text": "In 1997, the White House was forced to declassify a top-secret memorandum from 1962, officially signed by the Chairman of the Joint Chiefs of Staff. Known as Operation Northwoods, the plan proposed staging horrific acts of terrorism on American soil against American citizens to justify starting a foreign war. The declassified pages detail plans to hijack commercial airliners, sink US military naval vessels, and detonate explosives in major cities, framing foreign adversaries for the carnage. President John F. Kennedy personally rejected the horrifying operation. What other signed operations are still locked away inside military vaults? Tell me your thoughts in the comments below, share this video with a friend, and make sure to subscribe to Abyss Secrets for raw, declassified history.",
        "query": "military bunker dark corridor old files classified vintage"
    },
    {
        "id": "creature_baltic_sea_anomaly",
        "category": "creature",
        "series": "Baltic Sea Anomaly",
        "part": 1,
        "min_likes": 500,
        "title": "Divers Touched It at the Bottom of the Sea... Then Electronics Died 🌊 #Shorts",
        "text": "Three hundred feet beneath the Baltic Sea lies a massive, geometric disc-shaped structure spanning two hundred feet wide. In 2012, professional deep-sea divers descended to investigate the object directly. As soon as the divers approached within six hundred feet, their satellite phones, digital cameras, and underwater sonar equipment shut down simultaneously. When they swam away, everything turned back on. Samples chiseled from the object revealed it is composed of limonite and iron oxides that geologists say cannot be formed by natural marine processes. Beneath the structure, sonar detected a nine-hundred-foot runway-like gouge on the seafloor, as if a craft crashed and slid across the bedrock. Hit subscribe right now and like the video. If we reach 500 likes, Part 2 covers the private military contractor intervention. What do you think it is?",
        "query": "underwater ancient ruins deep sea sunken ship mysterious"
    },
    {
        "id": "cia_mkultra_blackbox",
        "category": "declassified",
        "series": "MKUltra Subproject 68",
        "part": 0,
        "min_likes": 0,
        "title": "The CIA Program That Erased Human Memories ⚠️ #Shorts #Declassified",
        "text": "This is official United States Senate document 95-103. Under CIA Subproject 68, the agency funded Dr. Ewen Cameron to develop a technique to completely erase human memory and rebuild personality from scratch. Unwitting patients admitted for minor anxiety were placed into drug-induced comas lasting up to eighty-six days, subjected to electroconvulsive shocks seventy times stronger than standard medical limits, and forced to listen to looped recorded messages half a million times. When the patients woke up, they had permanently forgotten their own names, their children, and how to speak. The agency attempted to incinerate the records in 1973, but thousands of pages were recovered. Subscribe to Abyss Secrets right now to uncover what governments hide, and share this with someone who needs to know the truth.",
        "query": "creepy dark vintage hospital old medical equipment classified"
    }
]

LONG_STORIES = [
    {
        "id": "long_abyss_monsters_expedition",
        "title": "Declassified Ocean: The Leviathans Roaming the Mariana Abyss",
        "text": "Thirty-six thousand feet beneath the ocean surface lies a realm of absolute darkness where the crushing weight of the water exceeds one thousand times the pressure at sea level. For centuries, oceanographers believed the aphotic hadal trenches were devoid of macroscopic life. Yet, unredacted deep-sea acoustic records tell a horrifying story. In 1960, during Jacques Piccard's legendary descent aboard the bathyscaphe Trieste, an unlogged biological collision occurred. Modern acoustic isolation techniques reveal the sound was an active organic echolocation burst emitted by a colossal apex predator roaming the abyssal plains. What prehistoric organisms survived in the dark? Subscribe to Abyss Secrets and leave your theories below.",
        "query": "deep sea dark ocean underwater trench mystery monster",
        "tags": ["ChallengerDeep", "MarianaTrench", "DeepSeaMonster", "DeclassifiedOcean", "AbyssSecrets", "Documentary"]
    },
    {
        "id": "long_cia_secret_experiments",
        "title": "Project MKUltra Declassified: The CIA's Mind Control Files Exposed",
        "text": "During the height of the Cold War, the Central Intelligence Agency orchestrated a covert program aimed at achieving absolute control over human cognition. Operating from safehouses and university laboratories, Project MKUltra subjected thousands of citizens to intense psychoactive substances, sensory deprivation, and aggressive conditioning. Though directives were issued to destroy all documentation, thousands of surviving files revealed a terrifying apparatus operating beyond ethical and constitutional limits. What else was hidden behind closed doors? Subscribe to Abyss Secrets for more raw historical revelations.",
        "query": "classified military documents old typewriter dark room interrogation",
        "tags": ["MKUltra", "CIADeclassified", "SecretProjects", "AbyssSecrets", "HistoricalDocumentary"]
    }
]

# ==================== TARIX VA ANALITIKA ====================
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {"uploaded_ids": data, "video_stats": {}}
                return data
        except Exception:
            return {"uploaded_ids": [], "video_stats": {}}
    return {"uploaded_ids": [], "video_stats": {}}

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# ==================== YOUTUBE AVTORIZATSIYA (XATOSIZ) ====================
def get_youtube_service():
    creds = None
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds or not creds.valid:
            if not os.path.exists("client_secret.json"):
                print("❌ XATOLIK: client_secret.json fayli topilmadi!")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            # port=0 tizimga bo'sh va ruxsat berilgan portni o'zi tanlashga imkon beradi
            creds = flow.run_local_server(port=0, open_browser=True)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def analyze_channel_performance(youtube):
    creature_views = 0
    declass_views = 0
    history = load_history()
    stats = history.get("video_stats", {})

    try:
        video_ids = list(stats.values())[-10:]
        if video_ids:
            res = youtube.videos().list(part="statistics", id=",".join(video_ids)).execute()
            for item in res.get("items", []):
                vid_id = item["id"]
                views = int(item["statistics"].get("viewCount", 0))
                for s_id, v_id in stats.items():
                    if v_id == vid_id:
                        story = next((s for s in SHORTS_STORIES if s["id"] == s_id), None)
                        if story:
                            if story["category"] == "creature":
                                creature_views += views
                            else:
                                declass_views += views
    except Exception as e:
        print(f"⚠️ Analitika bildirishnomasi: {e}")

    return "creature" if creature_views >= declass_views else "declassified"

def get_next_story(youtube, is_long=False):
    history = load_history()
    uploaded_ids = set(history.get("uploaded_ids", []))

    if is_long:
        available = [s for s in LONG_STORIES if s["id"] not in uploaded_ids]
        if not available:
            history["uploaded_ids"] = [i for i in history.get("uploaded_ids", []) if not i.startswith("long_")]
            available = LONG_STORIES
        return available[0]

    available = [s for s in SHORTS_STORIES if s["id"] not in uploaded_ids]
    if not available:
        history["uploaded_ids"] = [i for i in history.get("uploaded_ids", []) if i.startswith("long_")]
        available = SHORTS_STORIES

    preferred_category = analyze_channel_performance(youtube)
    print(f"📊 [Smart Algoritm]: Eng ko'p ko'rilayotgan toifa tanlandi: {preferred_category.upper()}")

    matched = [s for s in available if s.get("category") == preferred_category]
    return matched[0] if matched else available[0]

# ==================== OVOZ GENERATSIYASI ====================
async def generate_voice(text, filename="voice.mp3"):
    comm = edge_tts.Communicate(text, voice="en-US-ChristopherNeural", rate="-3%", pitch="-2Hz")
    await comm.save(filename)

# ==================== PEXELS VIDEO MATERIALLARI ====================
def download_pexels_clips(query, orientation="portrait", count=1, output_files=["bg.mp4"]):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&orientation={orientation}&per_page=15"
    resp = requests.get(url, headers=headers).json()
    videos = resp.get("videos", [])

    if not videos:
        fallback = "dark deep underwater" if orientation == "portrait" else "dark sea storm mystery"
        url = f"https://api.pexels.com/videos/search?query={fallback}&orientation={orientation}&per_page=15"
        videos = requests.get(url, headers=headers).json().get("videos", [])

    random.shuffle(videos)
    target_width, target_height = (1080, 1920) if orientation == "portrait" else (1920, 1080)

    for i in range(min(count, len(output_files))):
        choice = videos[i % len(videos)]
        video_files = choice["video_files"]
        selected = next((f for f in video_files if f.get("width") == target_width and f.get("height") == target_height), video_files[0])
        res = requests.get(selected["link"], stream=True)
        with open(output_files[i], "wb") as f:
            for chunk in res.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

# ==================== MONTAJ ====================
def build_short_video(audio_file="voice.mp3", video_file="bg.mp4", output_file="final_short.mp4"):
    audio = AudioFileClip(audio_file)
    dur = audio.duration + 0.4
    clip = VideoFileClip(video_file)

    if clip.duration < dur:
        clip = clip.loop(duration=dur)
    else:
        clip = clip.subclip(0, dur)

    final = clip.set_audio(audio)
    final.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=24, preset="ultrafast", verbose=False, logger=None)
    audio.close()
    clip.close()
    final.close()

def build_long_video(audio_file="voice_long.mp3", clip_files=["c1.mp4", "c2.mp4", "c3.mp4", "c4.mp4"], output_file="final_long.mp4"):
    audio = AudioFileClip(audio_file)
    dur = audio.duration + 0.5
    clips = [VideoFileClip(f) for f in clip_files]
    concatenated = concatenate_videoclips(clips, method="compose")

    if concatenated.duration < dur:
        final_video = concatenated.loop(duration=dur)
    else:
        final_video = concatenated.subclip(0, dur)

    final = final_video.set_audio(audio)
    final.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=24, preset="ultrafast", verbose=False, logger=None)
    audio.close()
    for c in clips:
        c.close()
    concatenated.close()
    final.close()

# ==================== YOUTUBE YUKLASH ====================
def upload_video_to_yt(youtube, video_path, story, is_shorts=True):
    title = story["title"]
    desc = story["text"] + "\n\n⚠️ Subscribe to Abyss Secrets for daily declassified reality.\n\n#Shorts #AbyssSecrets #DeepSea #Declassified #Mystery"
    tags = ["Shorts", "AbyssSecrets", "Horror", "Declassified", "DeepSea", "CIAFiles", "Unexplained"] if is_shorts else story["tags"]

    body = {
        "snippet": {
            "title": title,
            "description": desc,
            "tags": tags,
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")
    req = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    res = req.execute()
    vid_id = res["id"]

    history = load_history()
    history.setdefault("uploaded_ids", []).append(story["id"])
    history.setdefault("video_stats", {})[story["id"]] = vid_id
    save_history(history)

    print("\n" + "=" * 50)
    print(f"🚀 VIDEO CHIQARILDI: https://youtu.be/{vid_id}")
    print("=" * 50 + "\n")
    return vid_id

# ==================== ASOSIY PIPELINE ====================
def run_pipeline(mode="short"):
    youtube = get_youtube_service()

    if mode == "long":
        story = get_next_story(youtube, is_long=True)
        print(f"\n[🎬 2 MINUTLIK VIDEO]: {story['title']}")
        asyncio.run(generate_voice(story["text"], "voice_long.mp3"))
        clip_files = ["c1.mp4", "c2.mp4", "c3.mp4", "c4.mp4"]
        download_pexels_clips(story["query"], orientation="landscape", count=4, output_files=clip_files)
        build_long_video("voice_long.mp3", clip_files, "final_long.mp4")
        upload_video_to_yt(youtube, "final_long.mp4", story, is_shorts=False)
    else:
        story = get_next_story(youtube, is_long=False)
        print(f"\n[🚀 50s SMART SHORTS]: {story['title']}")
        asyncio.run(generate_voice(story["text"], "voice.mp3"))
        download_pexels_clips(story["query"], orientation="portrait", count=1, output_files=["bg.mp4"])
        build_short_video("voice.mp3", "bg.mp4", "final_short.mp4")
        upload_video_to_yt(youtube, "final_short.mp4", story, is_shorts=True)

if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "short"
    if mode_arg == "auth":
        get_youtube_service()
        print("✅ token.json muvaffaqiyatli saqlandi!")
    else:
        run_pipeline(mode_arg)