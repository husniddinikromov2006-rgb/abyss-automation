import os
import sys
import glob
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_RAW = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

def get_authenticated_service():
    if not CLIENT_SECRET_RAW or not REFRESH_TOKEN:
        print("[XATO]: YOUTUBE_CLIENT_SECRET yoki YOUTUBE_REFRESH_TOKEN GitHub Secrets'da topilmadi!")
        sys.exit(1)

    try:
        client_data = json.loads(CLIENT_SECRET_RAW)
        # Google JSON formati bo'yicha 'installed' yoki 'web' kalitini olish
        config = client_data.get("installed", client_data.get("web", {}))
        client_id = config.get("client_id")
        client_secret = config.get("client_secret")

        credentials = Credentials(
            None,
            refresh_token=REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        return build("youtube", "v3", credentials=credentials)
    except Exception as e:
        print(f"[XATO]: Google OAuth ulanishida xatolik: {e}")
        sys.exit(1)

def upload_videos():
    youtube = get_authenticated_service()
    video_files = glob.glob("output/*.mp4")

    if not video_files:
        print("[OGOHLANTIRISH]: output/ papkasida yuklash uchun video topilmadi.")
        return

    for file_path in video_files:
        file_name = os.path.basename(file_path)
        is_short = "Short" in file_name
        
        # Fayl nomidan sarlavha yasash
        clean_title = file_name.replace("_", " ").replace(".mp4", "")
        
        if is_short:
            title = f"{clean_title} #Shorts"
            tags = ["Shorts", "nature", "aesthetic", "travel", "4k", "relaxing"]
            desc = "Breathtaking nature scenery in 4K UHD. #Shorts #nature #cinematic"
        else:
            title = f"{clean_title} – Ultra HD Cinematic Nature (4K)"
            tags = ["nature", "cinematic", "scenic", "relaxing", "4k", "travel", "earth"]
            desc = "Immerse yourself in breathtaking 4K scenic landscapes and soothing atmosphere. #nature #cinematic #4k"

        body = {
            "snippet": {
                "title": title[:100],
                "description": desc,
                "tags": tags,
                "categoryId": "19"  # Travel & Events kategoriyasi
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        print(f"\nYouTube'ga yuklanmoqda: {file_name}")
        media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Jarayon: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        print(f"[MUVAFFAQIYAT]: Video joylandi! Havola: https://youtu.be/{video_id}")

if __name__ == "__main__":
    upload_videos()
