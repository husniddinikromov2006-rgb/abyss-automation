import os
import json
import time
import re
import random
import requests

REQUEST_TIMEOUT = 60

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

def extract_valid_json(text):
    start = text.find("{")
    if start == -1:
        raise ValueError("Matnda { topilmadi")

    depth = 0
    in_string = False
    escape = False

    for i in range(start, len(text)):
        char = text[i]
        if char == '"' and not escape:
            in_string = not in_string
        elif char == '\\' and in_string:
            escape = not escape
            continue

        if not in_string:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    return text[start:i+1]
        escape = False

    end = text.rfind("}")
    if end > start:
        return text[start:end+1]

    raise ValueError("To'liq yopilgan JSON bloki topilmadi")

def clean_json_response(raw_text):
    if not raw_text:
        raise ValueError("Bo'sh javob keldi.")

    text = str(raw_text).strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text).strip()

    json_candidate = extract_valid_json(text)
    data = json.loads(json_candidate)

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
You are an elite HBO documentary director. Write EPISODE {episode_num} of deep-sea military thriller (~520 words).
Theme: {winning_theme}. Forbidden titles: {past_titles_str}.
Return ONLY raw JSON:
{{
  "title": "ABYSS ARCHIVES - Episode {episode_num}: The Breach",
  "hook": "Telemetry lost at 40,000 feet.",
  "script": "Full narration script...",
  "scenes": [
    {{"text": "Line 1", "prompt": "16:9 photorealistic 8k dark deep ocean submarine hull horror, Unreal Engine 5"}}
  ]
}}
"""
    elif mode == "long_3min":
        return f"""
You are an elite documentary director. Write an intense 3-minute standalone military naval mystery (~400 words).
Theme: {winning_theme}. Forbidden titles: {past_titles_str}.
Return ONLY raw JSON:
{{
  "title": "Unidentified Deep Ocean Threat Under 70 Chars",
  "hook": "Sonar picked up impossible acoustics.",
  "script": "Full narrative script...",
  "scenes": [
    {{"text": "Line 1", "prompt": "16:9 photorealistic 8k dark underwater naval disaster, Unreal Engine 5"}}
  ]
}}
"""
    elif mode == "post":
        return f"""
Create a YouTube Community Post about classified deep sea exploration.
Theme: {winning_theme}. Return ONLY raw JSON:
{{
  "title": "Community Post Update",
  "text": "Declassified expedition log update ending with an intense question.",
  "image_prompt": "16:9 classified expedition underwater photo, dark ocean"
}}
"""
    else:
        return f"""
Write an intense US naval abyss horror story for YouTube Shorts (50 seconds, ~120 words).
Theme: {winning_theme}. Forbidden titles: {past_titles_str}.
Return ONLY raw JSON:
{{
  "title": "What Lurks Deep Below 🌊 #Shorts",
  "hook": "We thought the bottom was empty.",
  "script": "Full narrative script...",
  "scenes": [
    {{"text": "Line 1", "prompt": "vertical 9:16 photorealistic 8k dark underwater horror, Unreal Engine 5"}}
  ]
}}
"""

# ============================================================
# VALIDATION
# ============================================================

def validate_story(data, mode):
    if not isinstance(data, dict):
        raise ValueError("Natija JSON emas.")

    if mode == "post":
        text_val = data.get("text") or data.get("content") or "Declassified expedition log recovered from Mariana Trench."
        data["text"] = str(text_val)
        return data

    title_val = data.get("title") or data.get("video_title") or "THE ABYSS INCIDENT #Shorts"
    data["title"] = str(title_val)

    script_val = data.get("script") or data.get("narration") or data.get("story")
    if not script_val:
        raise ValueError("Script topilmadi.")
    data["script"] = str(script_val)

    hook_val = data.get("hook") or data["script"].split(".")[0]
    data["hook"] = str(hook_val)

    scenes = data.get("scenes") or data.get("shots") or []
    target_count = 12 if mode == "shorts" else (36 if mode == "long_3min" else 48)

    if not isinstance(scenes, list) or len(scenes) == 0:
        sentences = [s.strip() for s in data["script"].split(".") if len(s.strip()) > 3]
        scenes = []
        for i in range(target_count):
            txt = sentences[i % len(sentences)] if sentences else "The darkness expanded rapidly."
            scenes.append({
                "text": txt,
                "prompt": "16:9 photorealistic 8k dark deep ocean naval submarine horror scene, Unreal Engine 5"
            })

    for sc in scenes:
        if isinstance(sc, dict):
            sc.setdefault("text", "Telemetry was completely silent.")
            sc.setdefault("prompt", "16:9 photorealistic 8k dark deep ocean naval submarine horror scene, Unreal Engine 5")

    data["scenes"] = scenes
    return data

# ============================================================
# ONLINE INTERNET AI (Pollinations Free Endpoints)
# ============================================================

def fetch_internet_ai(prompt):
    endpoints = [
        "[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)",
        "[https://text.pollinations.ai/](https://text.pollinations.ai/)"
    ]

    # Usul 1: OpenAI JSON API
    try:
        url = clean_url(endpoints[0])
        payload = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": "You are a professional documentary script JSON generator. Output only valid raw JSON."},
                {"role": "user", "content": prompt}
            ]
        }
        r = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            res_data = r.json()
            if "choices" in res_data and len(res_data["choices"]) > 0:
                content = res_data["choices"][0].get("message", {}).get("content", "")
                if content:
                    return clean_json_response(content)
            elif "content" in res_data:
                return clean_json_response(res_data["content"])
    except Exception as e:
        print(f"⚠️ Internet AI (1-usul) kutilmoqda: {e}")

    # Usul 2: Direct URL GET
    try:
        url = clean_url(f"[https://text.pollinations.ai/](https://text.pollinations.ai/){requests.utils.quote(prompt)}?json=true")
        r = requests.get(url, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200 and r.text:
            return clean_json_response(r.text)
    except Exception as e:
        print(f"⚠️ Internet AI (2-usul) kutilmoqda: {e}")

    return None

# ============================================================
# OFFLINE EMERGENCY BACKUP (Har doim 100% kafolat)
# ============================================================

def generate_emergency_story(winning_theme, mode, episode_num=1):
    print("🚨 Internet uzilishiga qarshi avtonom syujet dvigateli ishga tushdi...")
    seed = random.randint(100, 999)

    hooks = [
        "At 36,000 feet below, our military sonar detected an impossible metallic heartbeat.",
        "Declassified US Navy logs reveal what really sank Submarine Echo-9.",
        "Something massive just passed beneath the deepest underwater trench.",
        "The deep sea research station went completely dark after recording this signal."
    ]

    selected_hook = random.choice(hooks)
    script = (
        f"{selected_hook} Telemetry indicated a structure larger than any known vessel moving silently along the oceanic seabed. "
        f"Initial military reports attributed the anomaly to thermal vents, but sound wave frequency matched advanced artificial propulsion. "
        f"When deep-diving drones descended into the fracture, all visual feeds corrupted simultaneously into blinding static. "
        f"The black box from expedition unit seven recorded a final transmission before dropping into the abyss. "
        f"Some secrets beneath the ocean floor were never meant to surface."
    )

    scenes_count = 12 if mode == "shorts" else (36 if mode == "long_3min" else 48)
    sentences = [s.strip() for s in script.split(".") if len(s.strip()) > 5]

    scenes = []
    aspect = "16:9" if mode in ["long_3min", "series_4min", "post"] else "9:16"
    prompts = [
        f"{aspect} photorealistic 8k dark deep ocean trench mystery submarine discovery, volumetric dark blue underwater lighting, Unreal Engine 5",
        f"{aspect} photorealistic 8k classified military submarine interior red alert lights, deep sea expedition disaster",
        f"{aspect} photorealistic 8k giant unknown mechanical structure partially buried in abyss ocean floor, cinematic horror",
        f"{aspect} photorealistic 8k deep sea exploration drone spotlight piercing murky black water, realistic particles"
    ]

    for i in range(scenes_count):
        txt = sentences[i % len(sentences)]
        p = prompts[i % len(prompts)]
        scenes.append({"text": txt, "prompt": p})

    title = f"DEEP ABYSS ANOMALY #{seed} #Shorts"
    if mode == "series_4min":
        title = f"ABYSS ARCHIVES - Episode {episode_num}: The Silent Signal"
    elif mode == "long_3min":
        title = f"The Unexplained Mariana Incident #{seed}"

    return {
        "title": title,
        "hook": selected_hook,
        "script": script,
        "scenes": scenes,
        "text": f"Expedition Log #{seed}: Signals detected at extreme depths. Did we awaken something that belongs to the abyss?"
    }

# ============================================================
# MAIN
# ============================================================

def get_unique_story(winning_theme, past_titles=None, past_hooks=None, mode="shorts", episode_num=1):
    past_titles = past_titles or []
    past_hooks = past_hooks or []

    prompt = build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num)

    # 1. Internetdagi ochiq AI
    print(f"🌐 Internetdagi ochiq AI tizimi ishga tushmoqda ({mode.upper()})...")
    result = fetch_internet_ai(prompt)
    if result:
        try:
            valid_data = validate_story(result, mode)
            print("✅ Internet AI ssenariyni muvaffaqiyatli yetkazdi.")
            return valid_data
        except Exception as e:
            print(f"⚠️ Internet AI JSON tekshiruvi: {e}")

    # 2. Favqulodda avtonom zaxira (Hech qachon xato bermaydi)
    fallback_data = generate_emergency_story(winning_theme, mode, episode_num)
    return validate_story(fallback_data, mode)
