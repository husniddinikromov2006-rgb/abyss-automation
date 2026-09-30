import os
import sys
import glob
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_RAW = os.getenv("YOUTUBE_TOKEN_JSON")

def get_authenticated_service():
    if not TOKEN_RAW:
        print("[XATO]: YOUTUBE_TOKEN_JSON GitHub Secrets ichida topilmadi!")
        sys.exit(1)

    try:
        token_data = json.loads(TOKEN_RAW)
        
        # Agar JSON ichida to'g'ridan-to'g'ri token parametrlari bo'lsa
        credentials = Credentials.from_authorized_user_info(token_data)
        return build("youtube", "v3", credentials=credentials)
    except Exception as e:
        print(f"[XATO]: Token orqali ulanishda xatolik: {e}")
        # Agar format sal boshqacha bo'lsa, qo'shimcha parametrlar bilan urinib ko'rish
        try:
            installed = token_data.get("installed", token_data.get("web", token_data))
            credentials = Credentials(
                token=token_data.get("access_token"),
                refresh_token=token_data.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=installed.get("client_id"),
                client_secret=installed.get("client_secret")
            )
            return build("youtube", "v3", credentials=credentials)
        except Exception as e2:
            print(f"[XATO]: Qayta ulanish ham o'xshamadi: {e2}")
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
        clean_title = file_name.replace("_", " ").replace(".mp4", "")
        
        if is_short:
            title = f"{clean_title} #Shorts"
            tags = ["Shorts", "nature", "aesthetic", "travel", "4k", "relaxing"]
            desc = "Breathtaking nature scenery in 4K UHD. #Shorts #nature #cinematic"
        else:
            title = f"{clean_title} – Ultra HD Cinematic Nature (4K)"
            tags = ["nature", "cinematic", "scenic", "relaxing", "4k", "travel", "earth"]
            desc = "Immerse yourself in breathtaking 4K scenic landscapes. #nature #cinematic #4k"

        body = {
            "snippet": {
                "title": title[:100],
                "description": desc,
                "tags": tags,
                "categoryId": "19"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        print(f"\nYouTube'ga yuklanmoqda: {file_name}...")
        media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Yuklanish foizi: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        print(f"[MUVAFFAQIYAT]: Video joylandi! Havola: https://youtu.be/{video_id}")

if __name__ == "__main__":
    upload_videos()
