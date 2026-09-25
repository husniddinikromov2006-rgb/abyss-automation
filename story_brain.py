import os
import json
import time
import re
import requests

try:
    from google import genai
except ImportError:
    genai = None

# ============================================================
# CONFIG
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
POLLINATIONS_URL = "https://text.pollinations.ai/"
REQUEST_TIMEOUT = 90

# ============================================================
# URL & JSON CLEANER
# ============================================================

def clean_url(url_str):
    if not url_str:
        return ""
    url_str = str(url_str).strip()
    match = re.search(r'https?://[^\s\)\]\"\']+', url_str)
    if match:
        return match.group(0)
    return url_str

def clean_json_response(raw_text):
    if not raw_text:
        raise ValueError("AI bo'sh javob qaytardi.")

    text = str(raw_text).strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text).strip()

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("AI javobi JSON obyekt emas.")
    return data

# ============================================================
# PROMPT
# ============================================================

def build_prompt(mode, winning_theme, past_titles=None, past_hooks=None, episode_num=1):
    past_titles = past_titles or []
    past_hooks = past_hooks or []

    past_titles_str = "\n- ".join(past_titles[-15:]) if past_titles else "None yet"
    past_hooks_str = "\n- ".join(past_hooks[-15:]) if past_hooks else "None yet"

    if mode == "series_4min":
        return f"""
You are an elite HBO/Netflix documentary director creating an episodic deep-sea military thriller.
Write EPISODE {episode_num}. Context: {winning_theme}.
Length: Strictly 4 minutes spoken pace (~520 words).
RULES:
1. Start with sudden classified military telemetry, sonar anomaly, or radio distress.
2. NO CLICHES.
3. Forbidden previous titles:
- {past_titles_str}
4. Forbidden previous hooks:
- {past_hooks_str}
5. Title MUST include: Episode {episode_num}:
6. End with an intense unresolved cliffhanger.
7. EXACTLY 48 scenes. Each scene needs "text" and "prompt".
8. Return ONLY raw valid JSON.

JSON FORMAT:
{{
  "title": "ABYSS ARCHIVES - Episode {episode_num}: Classified Submarine Breach",
  "hook": "First chilling spoken sentence",
  "script": "Full narration script (~520 words)",
  "scenes": [
    {{"text": "spoken narration line", "prompt": "16:9 photorealistic 8k dark cinematic deep ocean expedition horror scene, Unreal Engine 5, volumetric lighting"}}
  ]
}}
"""

    elif mode == "long_3min":
        return f"""
You are an elite Hollywood mystery director. Write an intense 3-minute horizontal naval documentary (~400 words).
Context: {winning_theme}.
RULES:
1. No cliché opening. Start with declassified naval logs or sonar emergency.
2. Forbidden previous titles:
- {past_titles_str}
3. Forbidden previous hooks:
- {past_hooks_str}
4. EXACTLY 36 scenes. Each scene needs "text" and "prompt".
5. Return ONLY raw valid JSON.

JSON FORMAT:
{{
  "title": "Compelling horizontal documentary title (under 70 chars)",
  "hook": "first intense spoken hook sentence",
  "script": "Full narrative script (~400 words)",
  "scenes": [
    {{"text": "spoken line", "prompt": "16:9 photorealistic 8k dark cinematic deep ocean naval disaster scene, Unreal Engine 5"}}
  ]
}}
"""

    elif mode == "post":
        return f"""
Create an intriguing Community Post for a deep ocean mystery YouTube channel.
Context: {winning_theme}. Return ONLY raw valid JSON.

JSON FORMAT:
{{
  "title": "Community Post Update",
  "text": "Intriguing declassified expedition report update ending with a question (~60-80 words).",
  "image_prompt": "16:9 cinematic classified black and white polaroid photograph of underwater expedition in dark ocean, 8k"
}}
"""

    else:
        return f"""
Write an intense US naval abyss horror story for YouTube Shorts (50 seconds spoken pace, ~120 words).
Context: {winning_theme}.
RULES:
1. NO CLICHES. Start with sudden emergency naval telemetry.
2. Forbidden titles:
- {past_titles_str}
3. Forbidden hooks:
- {past_hooks_str}
4. EXACTLY 12 scenes. Each scene needs "text" and "prompt".
5. Return ONLY raw valid JSON.

JSON FORMAT:
{{
  "title": "punchy title with emoji and #Shorts",
  "hook": "first 10 spoken words",
  "script": "Full narrative script (~120 words)",
  "scenes": [
    {{"text": "spoken line", "prompt": "vertical 9:16 photorealistic 8k dark underwater cinematic horror prompt"}}
  ]
}}
"""

# ============================================================
# VALIDATION
# ============================================================

def validate_story(data, mode):
    if not isinstance(data, dict):
        raise ValueError("Natija JSON object emas.")

    if mode == "post":
        if "text" not in data:
            raise ValueError("Post uchun matn topilmadi.")
        return data

    for field in ["title", "hook", "script"]:
        if not data.get(field):
            raise ValueError(f"JSON ichida '{field}' yo'q yoki bo'sh.")

    if "scenes" not in data or not isinstance(data["scenes"], list):
        raise ValueError("JSON ichida to'g'ri 'scenes' ro'yxati yo'q.")

    for i, scene in enumerate(data["scenes"], 1):
        if not isinstance(scene, dict):
            raise ValueError(f"{i}-scene dict formatida emas.")
        scene.setdefault("text", "The abyss remained silent.")
        scene.setdefault("prompt", "16:9 photorealistic dark deep ocean military horror scene, Unreal Engine 5")

    return data

# ============================================================
# GEMINI GENERATOR (Retry & Backoff)
# ============================================================

def generate_with_gemini(prompt):
    if not GEMINI_API_KEY or genai is None:
        return None

    try:
        print(f"🧠 Gemini ({GEMINI_MODEL}) ishga tushmoqda...")
        client = genai.Client(api_key=GEMINI_API_KEY)

        for attempt in range(1, 4):
            try:
                print(f"   Gemini urinish {attempt}/3...")
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )
                if response and response.text:
                    print("✅ Gemini javob berdi.")
                    return clean_json_response(response.text)
            except Exception as e:
                print(f"⚠️ Gemini urinish {attempt} xatosi: {e}")
                if attempt < 3:
                    time.sleep(4 * attempt)
    except Exception as e:
        print(f"⚠️ Gemini ishga tushmadi: {e}")

    return None

# ============================================================
# POLLINATIONS GENERATOR (Mutlaqo bepul, Kalitsiz!)
# ============================================================

def generate_with_pollinations(prompt):
    print("🧠 Pollinations zaxira AI ishga tushmoqda...")
    
    # 1-usul: OpenAI Endpoint orqali
    try:
        url = clean_url("[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)")
        payload = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": "You are a professional documentary script JSON generator. Output only valid raw JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        r = requests.post(url, json=payload, timeout=60)
        if r.status_code == 200:
            res_data = r.json()
            if "choices" in res_data and len(res_data["choices"]) > 0:
                content = res_data["choices"][0]["message"]["content"]
                return clean_json_response(content)
    except Exception as e:
        print(f"⚠️ Pollinations A usuli o'tmadi: {e}")

    # 2-usul: To'g'ridan-to'g'ri prompt jo'natish
    try:
        url = clean_url(f"[https://text.pollinations.ai/](https://text.pollinations.ai/){requests.utils.quote(prompt)}?json=true")
        r = requests.get(url, timeout=60)
        if r.status_code == 200 and r.text:
            return clean_json_response(r.text)
    except Exception as e:
        print(f"⚠️ Pollinations B usuli o'tmadi: {e}")

    return None

# ============================================================
# MAIN
# ============================================================

def get_unique_story(winning_theme, past_titles=None, past_hooks=None, mode="shorts", episode_num=1):
    past_titles = past_titles or []
    past_hooks = past_hooks or []

    prompt = build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num)

    # 1. Gemini
    result = generate_with_gemini(prompt)
    if result:
        try:
            return validate_story(result, mode)
        except Exception as e:
            print(f"⚠️ Gemini JSON validatsiya xatosi: {e}")

    # 2. Pollinations Fallback
    result = generate_with_pollinations(prompt)
    if result:
        try:
            return validate_story(result, mode)
        except Exception as e:
            print(f"⚠️ Pollinations JSON validatsiya xatosi: {e}")

    raise RuntimeError("AI tizimlaridan ssenariyni olib bo'lmadi!")
