import os
import json
import base64
import requests
import streamlit as st
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ============================================================
# SAHIFA SOZLAMALARI
# ============================================================
st.set_page_config(
    page_title="ABYSS BOSHQARUV MARKAZI // MAXFIY",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CYBER-ABYSS PREMIUM DIZAYN & CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

    /* Asosiy fon va shrift */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #061527 0%, #020712 60%, #000206 100%);
        color: #c8d6e5;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Asosiy sarlavha */
    .abyss-header {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00c6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 242, 254, 0.4);
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }

    .abyss-sub {
        font-size: 1.1rem;
        color: #576574;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 25px;
    }

    /* Glassmorphism Metrika Kartochkalari */
    .metric-box {
        background: rgba(8, 24, 48, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(0, 242, 254, 0.05);
        transition: all 0.3s ease;
    }
    .metric-box:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 242, 254, 0.6);
        box-shadow: 0 12px 40px 0 rgba(0, 242, 254, 0.2);
    }
    .metric-val {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #00f2fe;
        text-shadow: 0 0 12px rgba(0, 242, 254, 0.5);
    }
    .metric-label {
        font-size: 0.95rem;
        color: #8395a7;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Video tahlil kartalari */
    .video-card {
        background: rgba(10, 25, 47, 0.6);
        backdrop-filter: blur(12px);
        border-left: 4px solid #00f2fe;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .video-card:hover {
        border-left: 4px solid #ff0055;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.7);
    }

    /* Baholash nishonlari */
    .badge-viral {
        background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
        color: #fff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-shadow: 0 0 4px rgba(0,0,0,0.5);
    }
    .badge-high {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        color: #fff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .badge-stable {
        background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        color: #fff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
    }

    /* Tablar dizayni */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(13, 30, 56, 0.6);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 10px;
        color: #8395a7;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        padding: 8px 24px;
        transition: all 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(0, 242, 254, 0.2) 0%, rgba(79, 172, 254, 0.2) 100%) !important;
        border-color: #00f2fe !important;
        color: #00f2fe !important;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
    }

    /* Asosiy tugma */
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        width: 100%;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 20px rgba(0, 114, 255, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.01);
        box-shadow: 0 6px 30px rgba(0, 198, 255, 0.7);
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# MA'LUMOTLARNI ULASH
# ============================================================
GITHUB_TOKEN = os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY", "husniddinikromov2006-rgb/abyss-automation")

def get_youtube_service():
    token_raw = os.getenv("YOUTUBE_TOKEN_JSON")
    if not token_raw:
        if os.path.exists("token.json"):
            with open("token.json", "r") as f:
                token_raw = f.read()
        else:
            return None
    try:
        info = json.loads(token_raw)
        creds = Credentials.from_authorized_user_info(info)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return build("youtube", "v3", credentials=creds)
    except Exception:
        return None

def translate_to_uzbek(text):
    if not text:
        return "Matn mavjud emas."
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q=" + requests.utils.quote(text[:1200])
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            res = r.json()
            return "".join([part[0] for part in res[0]])
    except Exception:
        pass
    return text

def load_file_from_github(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    if not GITHUB_TOKEN:
        return {}
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{filepath}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = base64.b64decode(r.json()["content"]).decode("utf-8")
        return json.loads(content)
    return {}

def save_instructions_to_github(data):
    filepath = "user_instructions.json"
    content_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content_str)
    except Exception:
        pass

    if not GITHUB_TOKEN:
        return True, "Mahalliy xotiraga saqlandi (GitHub PAT ulanmagan)"
        
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{filepath}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    
    sha = None
    r_get = requests.get(url, headers=headers)
    if r_get.status_code == 200:
        sha = r_get.json()["sha"]

    payload = {
        "message": "Update bot directives via Command Center [skip ci]",
        "content": base64.b64encode(content_str.encode("utf-8")).decode("utf-8"),
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    r_put = requests.put(url, headers=headers, json=payload)
    if r_put.status_code in [200, 201]:
        return True, "Buyruqlar bulut tizimiga muvaffaqiyatli yetkazildi!"
    return False, f"Xatolik yuz berdi: {r_put.text}"

# ============================================================
# ASOSIY PANEL
# ============================================================
st.markdown('<div class="abyss-header">ABYSS SECRETS // BOSHQARUV MARKAZI</div>', unsafe_allow_html=True)
st.markdown('<div class="abyss-sub">Neyrotizimli boshqaruv, video auditi va sun\'iy intellekt tahlili</div>', unsafe_allow_html=True)

tab_analytics, tab_translate, tab_directives = st.tabs([
    "📊 ANALITIKA VA VIDEO STATUSI",
    "🇺🇿 O'ZBEKCHA MAZMUN VA MATNLAR",
    "🎮 BOTGA BUYRUQ BERISH MARKAZI"
])

# ----------------- TAB 1: ANALITIKA -----------------
with tab_analytics:
    yt = get_youtube_service()
    history = load_file_from_github("history.json")

    if not yt:
        st.warning("⚠️ YouTube API ulanmadi. Tizim mahalliy tarix bilan ko'rsatilmoqda.")
    else:
        try:
            req = yt.channels().list(part="contentDetails,statistics", mine=True)
            res = req.execute()
            ch_stats = res["items"][0]["statistics"]

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val">{int(ch_stats.get('viewCount', 0)):,}</div>
                    <div class="metric-label">Jami Ko'rishlar</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val">{int(ch_stats.get('subscriberCount', 0)):,}</div>
                    <div class="metric-label">Obunachilar</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val">{ch_stats.get('videoCount', 0)}</div>
                    <div class="metric-label">Yuklangan Videolar</div>
                </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val">100%</div>
                    <div class="metric-label">Avtopilot Holati</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("<br>", unsafe_allow_html=True)
            
            uploads_id = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            pl_req = yt.playlistItems().list(part="snippet", playlistId=uploads_id, maxResults=15)
            pl_res = pl_req.execute()
            
            v_ids = [item["snippet"]["resourceId"]["videoId"] for item in pl_res.get("items", [])]
            if v_ids:
                v_req = yt.videos().list(part="snippet,statistics", id=",".join(v_ids))
                v_res = v_req.execute()

                st.markdown("### 📡 So'nggi yuklangan videolar auditi")
                for item in v_res.get("items", []):
                    title = item["snippet"]["title"]
                    stats = item.get("statistics", {})
                    views = int(stats.get("viewCount", 0))
                    likes = int(stats.get("likeCount", 0))
                    comments = int(stats.get("commentCount", 0))
                    thumb = item["snippet"]["thumbnails"]["medium"]["url"]
                    vid_id = item["id"]

                    score = views + (likes * 10)
                    if score > 800:
                        badge = '<span class="badge-viral">⚡ O\'TA YUQORI (VIRAL)</span>'
                    elif score > 200:
                        badge = '<span class="badge-high">🔥 A\'LO NATIJA</span>'
                    else:
                        badge = '<span class="badge-stable">⚖️ QONIQARLI TEZLIK</span>'

                    st.markdown(f"""
                    <div class="video-card">
                        <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
                            <img src="{thumb}" style="width: 140px; border-radius: 8px; border: 1px solid rgba(0,242,254,0.3);">
                            <div style="flex: 1;">
                                <div style="font-size: 1.25rem; font-weight: 700; color: #fff;">
                                    <a href="https://youtu.be/{vid_id}" target="_blank" style="color: #00f2fe; text-decoration: none;">{title}</a>
                                </div>
                                <div style="margin-top: 6px; font-size: 0.95rem; color: #a4b0be;">
                                    Ko'rishlar: <b style="color: #fff;">{views:,}</b> | 
                                    Layklar: <b style="color: #fff;">{likes:,}</b> | 
                                    Izohlar: <b style="color: #fff;">{comments}</b>
                                </div>
                                <div style="margin-top: 8px;">{badge}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Analitika ma'lumotlarini olishda xatolik: {e}")

# ----------------- TAB 2: O'ZBEKCHA TARJIMA VA MATN -----------------
with tab_translate:
    st.markdown("### 🇺🇿 Inglizcha videolarning o'zbekcha to'liq tushuntirishi")
    h_data = load_file_from_github("history.json")
    titles = h_data.get("past_titles", [])
    hooks = h_data.get("past_hooks", [])

    if not titles:
        st.info("Tarixda videolar ro'yxati hali shakllanmagan.")
    else:
        for idx in range(min(12, len(titles))):
            t = titles[-(idx+1)]
            h = hooks[-(idx+1)] if idx < len(hooks) else "Ma'lumot yo'q"

            with st.expander(f"🎬 #{len(titles)-idx}: {t}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**🇺🇸 Asl inglizcha (English):**")
                    st.code(f"Title: {t}\nHook: {h}", language="markdown")
                with c2:
                    st.markdown("**🇺🇿 O'zbekcha mazmuni:**")
                    with st.spinner("Tarjima qilinmoqda..."):
                        uz_t = translate_to_uzbek(t)
                        uz_h = translate_to_uzbek(h)
                    st.success(f"📌 **Sarlavha:** {uz_t}")
                    st.info(f"⚡ **Boshlanish jumlasi (Hook):** {uz_h}")

# ----------------- TAB 3: BOTGA BUYRUQ MARKAZI -----------------
with tab_directives:
    st.markdown("### 🎮 Neyrotizimga maxsus ko'rsatma va talablar kiritish")
    st.markdown("Bu yerga yozgan talablaringiz saqlanadi va bot keyingi videolarni faqat shu yo'nalishda generatsiya qiladi.")

    cfg = load_file_from_github("user_instructions.json")

    with st.form("custom_directives_panel"):
        user_prompt = st.text_area(
            "✍️ Maxsus talab yoki yo'nalishni yozing (O'zbekcha):",
            value=cfg.get("custom_prompt", "Barcha kadrlarda suvosti yirtqichlari ulkan va g'avvoslar bilan to'qnashuv sahnasi bo'lsin."),
            height=120,
            help="Masalan: 'Faqat 2 qismli harbiy suvosti kemasi halokati bo'lsin', 'Tinch kadrlarni umuman qo'shma'"
        )

        col1, col2 = st.columns(2)
        with col1:
            horror_mode = st.select_slider(
                "💀 Qo'rquv va adrenalin darajasi:",
                options=["Oddiy hujjatli film", "Kuchli mistika", "Tubsiz dahshat (Ekstremal Abyss)"],
                value=cfg.get("horror_level", "Tubsiz dahshat (Ekstremal Abyss)")
            )
        with col2:
            main_focus = st.selectbox(
                "🎯 Asosiy e'tibor qaratiladigan obyekt:",
                options=[
                    "Ulkan Maxluqlar va Yirtqichlar (Monsters)",
                    "Halokatga uchragan Yadroviy Kemalar (Submarines)",
                    "Maxfiy Harbiy Ekspeditsiyalar (Military Secrets)",
                    "Okean tubidagi Notanish Obyektlar (Alien Base)"
                ],
                index=0
            )

        prohibited = st.text_input(
            "🚫 Umuman ishlatilmasin (Taqiqlangan mavzular):",
            value=cfg.get("prohibited_topics", "kulgili kadrlar, oddiy baliqlar, quyosh nuri")
        )

        submit_btn = st.form_submit_button("🔱 BUYRUQLARNI TIZIMGA YUBORISH VA SAQLASH")
        if submit_btn:
            new_data = {
                "custom_prompt": user_prompt,
                "horror_level": horror_mode,
                "target_focus": main_focus,
                "prohibited_topics": prohibited,
                "updated_at": str(os.getenv("GITHUB_RUN_ID", "dashboard"))
            }
            ok, msg = save_instructions_to_github(new_data)
            if ok:
                st.success(f"✅ {msg}")
                st.balloons()
            else:
                st.error(f"❌ {msg}")
