import os
import json
import random
import sys
import asyncio
import datetime
from zoneinfo import ZoneInfo
import requests
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ==================== SOZLAMALAR ====================
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "EdoUks31ZIxOOLAE35gYGpgiP3ikgDFZBiTlmDEievg9OUnR87AGxoLX")
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]
HISTORY_FILE = "history.json"
US_TIMEZONE = ZoneInfo("America/New_York")

# ==================== 1. SHORTS BAZASI (45-55s, VERTIKAL) ====================
SHORTS_STORIES = [
    {
        "id": "mariana_part1",
        "type": "multi",
        "series": "Mariana Trench Depth Anomaly",
        "part": 1,
        "niche": "ocean",
        "min_likes": 5000,
        "title": "What Lurks at 36,000 Feet Below? - Part 1 🌊 #Shorts #AbyssSecrets",
        "text": "At thirty-six thousand feet below the Pacific Ocean, pressure reaches over eight tons per square inch, and natural sunlight has never touched the seabed. In 1960, a research vessel lowered an ultra-sensitive acoustic sonar array directly into the Challenger Deep. For three hours, there was absolute dead silence. Then, without warning, the hydrophones registered an echo from an organic biological entity measuring eight hundred feet in length, ascending vertically toward the ship at an impossible speed. The water temperature plummeted fifteen degrees in seconds before the audio cut out completely. If this video gets 5,000 likes, we unlock the classified Part 2 with the decoded black box audio. Hit like and subscribe right now so you do not miss the truth.",
        "query": "deep sea dark ocean underwater"
    },
    {
        "id": "mariana_part2",
        "type": "multi",
        "series": "Mariana Trench Depth Anomaly",
        "part": 2,
        "niche": "ocean",
        "min_likes": 0,
        "title": "The Mariana Trench Creature - Part 2 🌊 #Shorts #AbyssSecrets",
        "text": "Continuing Part 1: As the crew initiated emergency ballast release, the eight-hundred-foot sonar signature circled the submarine three times before plunging down into an unmapped oceanic chasm far below the trench floor. When the vessel surfaced and engineers inspected the exterior, they discovered claw-like grooves gouged four inches deep directly into the solid titanium hull. Marine biologists still maintain that no known creature could withstand that crushing pressure, let alone generate that physical force. What ancient leviathan is sleeping in our oceans? Subscribe to Abyss Secrets to unlock more declassified oceanic horrors.",
        "query": "deep ocean dark sea underwater"
    },
    {
        "id": "bermuda_pyramids_single",
        "type": "single",
        "series": "Bermuda Megaliths",
        "part": 0,
        "niche": "ocean",
        "min_likes": 0,
        "title": "The Sunken Pyramids Beneath Bermuda ⚠️ #Shorts #MysteryFacts",
        "text": "The Bermuda Triangle is notorious for missing ships and planes, but modern deep-sea sonar scans recently revealed something far more terrifying. Resting two thousand meters beneath the ocean floor are colossal, perfectly smooth structures resembling giant glass pyramids. Oceanographers noted that direct flyovers cause all satellite telemetry, electronic gyro-compasses, and radio transmitters to fail simultaneously. Thermal sensors detect localized pulsating electromagnetic energy radiating straight from the apex. Are these artifacts remnants of an advanced lost civilization, or something not from this Earth? Share your theory in the comments and subscribe for daily revelations.",
        "query": "dark stormy ocean lightning underwater"
    },
    {
        "id": "saturn_part1",
        "type": "multi",
        "series": "Saturn Transmission",
        "part": 1,
        "niche": "space",
        "min_likes": 10000,
        "title": "NASA's Unexplained Saturn Audio - Part 1 🪐 #Shorts #SpaceHorror",
        "text": "Space is supposed to be absolute vacuum silence, but when NASA's Cassini probe entered orbit around Saturn, its plasma wave instrument intercepted complex radio emissions echoing from the planet's atmosphere. When engineers converted these frequencies into audible sound, the recording produced pulsating rhythmic oscillations that sound eerily like thousands of choral voices echoing inside a cosmic cavern. Physicists are baffled by the repeating mathematical patterns hidden within the noise. If this video reaches 10,000 likes, we drop Part 2 breaking down the decoded frequency spectrum. Hit subscribe right now to keep exploring the deep void.",
        "query": "saturn planet deep space galaxy"
    },
    {
        "id": "saturn_part2",
        "type": "multi",
        "series": "Saturn Transmission",
        "part": 2,
        "niche": "space",
        "min_likes": 0,
        "title": "The Hexagon Storm Engine - Part 2 🪐 #Shorts #SpaceHorror",
        "text": "Continuing Part 1: Spectroscopic scans proved that these chilling transmissions emanate directly from Saturn's North Pole—a perpetual geometric hurricane measuring twenty thousand miles wide. In fluid dynamics, nature does not create straight hexagonal angles in turbulent gases. Yet this storm has maintained its exact geometry for centuries, firing synchronized electromagnetic pulses deep into the void. Could the core of this gas giant conceal an ancient alien megastructure? Drop your thoughts below and subscribe to Abyss Secrets for daily cosmic truths.",
        "query": "deep space galaxy nebula stars"
    },
    {
        "id": "rogue_planets_single",
        "type": "single",
        "series": "Rogue Planets",
        "part": 0,
        "niche": "space",
        "min_likes": 0,
        "title": "The Ghost Worlds Wandering in the Dark 🌑 #Shorts #SpaceMysteries",
        "text": "There are billions of nomad planets hurtling through the interstellar void completely detached from any parent star. These rogue worlds wander in perpetual freezing darkness with surfaces coated in solid nitrogen and deep oceans sealed beneath miles of tectonic ice. If one ever passes through our solar system, we would not detect it until its immense gravitational pull began tearing Earth from its orbit, plunging humanity into endless winter. Subscribe to Abyss Secrets to unlock more terrifying universe facts.",
        "query": "black space void dark galaxy"
    },
    {
        "id": "kola_part1",
        "type": "multi",
        "series": "Kola Borehole Mystery",
        "part": 1,
        "niche": "earth",
        "min_likes": 7000,
        "title": "Drilling to the Gates of Earth - Part 1 ⛏️ #Shorts #CreepyStories",
        "text": "In the remote Russian tundra, scientists spent twenty-four years drilling the deepest artificial hole in history, boring over forty thousand feet into the continental crust. Seven miles down, the heavy industrial drill suddenly began spinning freely as if breaking into a colossal subterranean cavern. When geologists lowered heat-resistant audio sensors to capture tectonic movements, they recorded horrifying acoustics. If this video gets 7,000 likes, we release Part 2 analyzing what they actually heard. Hit like and subscribe right now so you do not miss it.",
        "query": "dark cavern magma deep cave fire"
    },
    {
        "id": "kola_part2",
        "type": "multi",
        "series": "Kola Borehole Mystery",
        "part": 2,
        "niche": "earth",
        "min_likes": 0,
        "title": "The Screams Beneath the Crust - Part 2 ⛏️ #Shorts #CreepyStories",
        "text": "Continuing Part 1: The acoustic sensors transmitted sounds resembling thousands of distressed human voices reverberating in high-density chambers. Within forty-eight hours of logging the recording, drilling was permanently halted, the borehole was sealed with a welded steel plate, and the entire facility was evacuated. Official reports blamed extreme temperatures, but the original tapes remain under state lock and key. What did they breach beneath our feet? Subscribe to Abyss Secrets for more forbidden knowledge.",
        "query": "dark smoke mysterious cavern underground"
    },
    {
        "id": "point_nemo_single",
        "type": "single",
        "series": "Point Nemo Abyss",
        "part": 0,
        "niche": "ocean",
        "min_likes": 0,
        "title": "Point Nemo: The Deep Ocean Graveyard 🌊 #Shorts #OceanMysteries",
        "text": "Point Nemo is the most isolated place on Earth, where the closest living humans are astronauts orbiting on the International Space Station. Because of its extreme isolation, space agencies intentionally crash decommissioned space stations and satellites straight into its waters. But beneath four miles of ocean, military sonar buoys recorded underwater heat signatures and moving masses larger than any known biological creature. What is really hiding in the deepest oceanic graveyard? Leave your comment and subscribe to Abyss Secrets.",
        "query": "point nemo dark ocean sea waves"
    }
]

# ==================== 2. TO'LIQ DOKUMENTAL VIDEOLAR (~2 DAQIQA, GORIZONTAL 16:9) ====================
LONG_STORIES = [
    {
        "id": "long_mariana_documentary",
        "title": "The Mariana Trench Secret: What Lies 36,000 Feet Below?",
        "text": "Thirty-six thousand feet beneath the western Pacific Ocean lies the Challenger Deep, a subterranean abyss so remote and hostile that more humans have walked on the surface of the moon than have ventured to its floor. The pressure here is crushing, exceeding one thousand times atmospheric weight, enough to compress a nuclear submarine like an aluminum can. For decades, orthodox marine science claimed this aphotic zone was devoid of complex macroscopic life. Yet, declassified naval sonar expeditions from the late twentieth century paint a dramatically different, far more disturbing picture. In 1960, during Jacques Piccard's historic descent aboard the Trieste bathyscaphe, an unlogged incident occurred. At approximately thirty-two thousand feet, the exterior hydrophones picked up a rhythmic acoustic signature echoing off the abyssal cliffs. Modern acoustic filtering reveals this was not tectonic grinding, nor was it thermal vent cavitation. It was the acoustic resonance of a biological entity of immense proportions moving with coordinated intent. When unmanned deep-sea probes returned to the coordinates decades later, they photographed anomalous claw-like gouges etched into the basaltic seabed and discovered hydrothermal vents spewing chemical isotopes unknown to terrestrial geology. Could the deepest trenches of our planet harbor ancient apex organisms that survived prehistoric extinction events? As deep ocean mapping programs continue, the abyss continues to remind us that humanity has only explored less than five percent of our oceans. Subscribe to Abyss Secrets and leave your thoughts in the comments below.",
        "query": "deep sea dark ocean underwater trench mystery",
        "tags": ["MarianaTrench", "AbyssSecrets", "DeepSeaCreatures", "OceanDocumentary", "UnexplainedMysteries"]
    },
    {
        "id": "long_point_nemo_spacecraft",
        "title": "Point Nemo: Earth's Most Terrifying and Isolated Coordinate",
        "text": "Located in the southern Pacific Ocean, Point Nemo is mathematically defined as the oceanic pole of inaccessibility. If you were to stand at these coordinates, the nearest dry land would be over two thousand six hundred kilometers away, meaning that at certain times of the day, the closest human beings to your location are astronauts aboard the International Space Station, orbiting four hundred kilometers above in low Earth orbit. Because this oceanic desert contains virtually no biological nutrients or commercial shipping lanes, international space agencies selected it as the designated spacecraft cemetery. Over two hundred and sixty defunct spacecraft, including Russia's Mir space station and hundreds of cargo freighters, lie shattered and sunken beneath four thousand meters of water. However, the abyss beneath Point Nemo hides secrets far older than the space age. In 1997, ultra-low frequency hydrophone networks across thousands of miles recorded the infamous Bloop sound, an organic underwater acoustic event originating mere hundreds of miles from the coordinate center. Military satellite sensors repeatedly detect localized geomagnetic variations and thermal disturbances shifting beneath the seabed at velocities impossible for underwater currents. What ancient forces or structures lie buried among the titan debris of fallen space stations? The deeper we look into our planet's loneliest waters, the more questions arise. Subscribe to Abyss Secrets for more untold investigations into the unknown.",
        "query": "ocean deep storm waves dark underwater satellite",
        "tags": ["PointNemo", "SpaceCemetery", "OceanMysteries", "TheBloop", "AbyssSecrets", "Documentary"]
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

# ==================== YOUTUBE AVTORIZATSIYA ====================
def get_youtube_service():
    creds = None
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("client_secret.json"):
                print("❌ XATOLIK: client_secret.json fayli papkada topilmadi!")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            try:
                creds = flow.run_local_server(port=8080, open_browser=True)
            except Exception:
                print("\n⚠️ Lokal port band. Konsol rejimiga o'tilmoqda...")
                creds = flow.run_console()

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def check_video_likes(youtube, video_id):
    try:
        res = youtube.videos().list(part="statistics", id=video_id).execute()
        if res.get("items"):
            return int(res["items"][0]["statistics"].get("likeCount", 0))
    except Exception:
        pass
    return 0

def get_next_story(is_long=False):
    history = load_history()
    uploaded_ids = set(history.get("uploaded_ids", []))
    video_stats = history.get("video_stats", {})

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

    youtube = None
    try:
        youtube = get_youtube_service()
    except Exception:
        pass

    for s in available:
        if s.get("type") == "multi" and s.get("part") == 2:
            prev_story = next((p for p in SHORTS_STORIES if p.get("series") == s.get("series") and p.get("part") == 1), None)
            if prev_story and prev_story["id"] in uploaded_ids:
                prev_video_id = video_stats.get(prev_story["id"])
                likes = check_video_likes(youtube, prev_video_id) if (youtube and prev_video_id) else 0
                if likes >= prev_story.get("min_likes", 0) or likes > 0:
                    return s

    return available[0]

# ==================== OVOZ GENERATSIYASI ====================
async def generate_voice(text, filename="voice.mp3"):
    comm = edge_tts.Communicate(text, voice="en-US-ChristopherNeural", rate="-3%", pitch="-3Hz")
    await comm.save(filename)

# ==================== PEXELS VIDEO YUKLASH ====================
def download_pexels_clips(query, orientation="portrait", count=1, output_files=["bg.mp4"]):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&orientation={orientation}&per_page=15"
    resp = requests.get(url, headers=headers).json()
    videos = resp.get("videos", [])

    if not videos:
        url = f"https://api.pexels.com/videos/search?query=dark+ocean&orientation={orientation}&per_page=15"
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
    dur = audio.duration + 0.5
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

# ==================== YOUTUBE'GA YUKLASH ====================
def upload_video_to_yt(video_path, story, is_shorts=True):
    youtube = get_youtube_service()
    title = story["title"]
    description = story["text"] + "\n\n#Shorts #AbyssSecrets #DeepSea #SpaceHorror" if is_shorts else story["text"] + "\n\nSubscribe to Abyss Secrets."
    tags = ["Shorts", "AbyssSecrets", "Horror", "Mystery", "DeepSea"] if is_shorts else story["tags"]

    body = {
        "snippet": {
            "title": title,
            "description": description,
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
    print(f"🚀 VIDEO YUKLANDI: https://youtu.be/{vid_id}")
    print("=" * 50 + "\n")
    return vid_id

# ==================== PIPELINE BOSHQARUVI ====================
def run_pipeline(mode="short"):
    if mode == "long":
        story = get_next_story(is_long=True)
        print(f"\n[🎬 2 MINUTLIK VIDEO]: {story['title']}")
        asyncio.run(generate_voice(story["text"], "voice_long.mp3"))
        clip_files = ["c1.mp4", "c2.mp4", "c3.mp4", "c4.mp4"]
        download_pexels_clips(story["query"], orientation="landscape", count=4, output_files=clip_files)
        build_long_video("voice_long.mp3", clip_files, "final_long.mp4")
        upload_video_to_yt("final_long.mp4", story, is_shorts=False)
    else:
        story = get_next_story(is_long=False)
        print(f"\n[🚀 SHORTS]: {story['title']}")
        asyncio.run(generate_voice(story["text"], "voice.mp3"))
        download_pexels_clips(story["query"], orientation="portrait", count=1, output_files=["bg.mp4"])
        build_short_video("voice.mp3", "bg.mp4", "final_short.mp4")
        upload_video_to_yt("final_short.mp4", story, is_shorts=True)

if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "short"
    if mode_arg == "auth":
        get_youtube_service()
        print("✅ token.json muvaffaqiyatli saqlandi!")
    else:
        run_pipeline(mode_arg)