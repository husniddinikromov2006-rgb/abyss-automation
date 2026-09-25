import os
import json
import time
import re
import random
import requests

REQUEST_TIMEOUT = 60

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

    raise ValueError("To'liq JSON bloki topilmadi")

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
        raise ValueError("AI javobi JSON emas.")
    return data

def build_prompt(mode, winning_theme, past_titles=None, past_hooks=None, episode_num=1):
    past_titles_str = "\n- ".join(past_titles[-15:]) if past_titles else "None yet"
    past_hooks_str = "\n- ".join(past_hooks[-15:]) if past_hooks else "None yet"

    style_guide = (
        "VISUAL STYLE: Extreme deep sea abyss horror, colossal bioluminescent sea monsters, "
        "diver flashlights cutting through pitch-black water, decaying submarine wreckage, "
        "terrifying tentacles, razor-sharp abyssal predators, hyperrealistic textures, cinematic lighting, 8k, Unreal Engine 5."
    )

    if mode == "series_4min":
        return f"""
You are a master of Lovecraftian deep-ocean suspense documentaries.
Write EPISODE {episode_num} of deep-sea military thriller (~520 words).
Theme: {winning_theme}. Forbidden titles: {past_titles_str}.
{style_guide}
Return ONLY raw valid JSON:
{{
  "title": "ABYSS ARCHIVES - Episode {episode_num}: The Mariana Breach",
  "hook": "At 36,000 feet, sonar detected a heartbeat.",
  "script": "Full narrative...",
  "scenes": [
    {{"text": "Line 1", "prompt": "16:9 photorealistic 8k colossal deep sea abyss sea monster lurking near research submarine, underwater headlights, terrifying jaws, dark murky water, Unreal Engine 5"}}
  ]
}}
"""
    elif mode == "long_3min":
        return f"""
Write an intense 3-minute standalone military naval mystery documentary (~400 words).
Theme: {winning_theme}. Forbidden titles: {past_titles_str}.
{style_guide}
Return ONLY raw valid JSON:
{{
  "title": "What Lurks Beneath Mariana Trench: Declassified Logs",
  "hook": "The submarine hull buckled before sonar went dead.",
  "script": "Full narrative...",
  "scenes": [
    {{"text": "Line 1", "prompt": "16:9 photorealistic 8k giant deep sea abyssal beast opening mouth in pitch black ocean trench, diver spotlight, cinematic horror, Octane render"}}
  ]
}}
"""
    elif mode == "post":
        return f"""
Create a viral Community Post update about deep ocean anomalies.
Theme: {winning_theme}.
Return ONLY raw valid JSON:
{{
  "title": "Community Post Update",
  "text": "Declassified expedition log recovered from 11,000 meters deep. What do you think attacked the hull?",
  "image_prompt": "16:9 cinematic underwater photograph of terrifying gigantic deep ocean monster approaching submarine window, dark ocean, 8k"
}}
"""
    else:
        return f"""
Write an ultra-viral 50-second US naval abyss horror story for YouTube Shorts (~120 words).
Theme: {winning_theme}. Forbidden titles: {past_titles_str}.
{style_guide}
Return ONLY raw valid JSON:
{{
  "title": "Never Dive Alone Into The Mariana Trench 🌊 #Shorts",
  "hook": "We thought the sonar echo was a mountain.",
  "script": "Full narrative...",
  "scenes": [
    {{"text": "Line 1", "prompt": "vertical 9:16 photorealistic 8k terrifying gigantic abyss sea monster with glowing eyes emerging from deep underwater trench, diver flashlight beam, cinematic horror, Unreal Engine 5"}}
  ]
}}
"""

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

    aspect = "16:9" if mode in ["long_3min", "series_4min", "post"] else "9:16"

    horror_prompts = [
        f"{aspect} photorealistic 8k gigantic terrifying deep sea leviathan serpent opening massive maw in dark ocean trench, diver flashlight beam hitting scales, hyperdetailed, Unreal Engine 5",
        f"{aspect} photorealistic 8k massive ancient cephalopod monster with tentacles wrapping around sunken military submarine, bioluminescent glowing runes, dark murky abyss, cinematic horror",
        f"{aspect} photorealistic 8k deep sea exploration diver floating into pitch black abyss staring at colossal glowing eye in oceanic trench, hyperrealistic volumetric fog",
        f"{aspect} photorealistic 8k horrifying deep sea anglerfish predator with razor teeth emerging from underwater abyss, bioluminescent lure illuminating dark water, cinematic depth"
    ]

    if not isinstance(scenes, list) or len(scenes) == 0:
        sentences = [s.strip() for s in data["script"].split(".") if len(s.strip()) > 3]
        scenes = []
        for i in range(target_count):
            txt = sentences[i % len(sentences)] if sentences else "The creature circled back."
            scenes.append({"text": txt, "prompt": horror_prompts[i % len(horror_prompts)]})

    for i, sc in enumerate(scenes):
        if isinstance(sc, dict):
            sc.setdefault("text", "The sonar recorded impossible movements.")
            p = sc.get("prompt", "")
            if len(p) < 25 or "ocean" not in p.lower():
                sc["prompt"] = horror_prompts[i % len(horror_prompts)]

    data["scenes"] = scenes
    return data

def fetch_internet_ai(prompt):
    endpoints = [
        "[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)",
        "[https://text.pollinations.ai/](https://text.pollinations.ai/)"
    ]

    try:
        url = clean_url(endpoints[0])
        payload = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": "You are an elite cinematic YouTube horror documentary creator. Output strictly raw JSON."},
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
        print(f"⚠️ Internet AI 1-usul: {e}")

    try:
        url = clean_url(f"[https://text.pollinations.ai/](https://text.pollinations.ai/){requests.utils.quote(prompt)}?json=true")
        r = requests.get(url, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200 and r.text:
            return clean_json_response(r.text)
    except Exception as e:
        print(f"⚠️ Internet AI 2-usul: {e}")

    return None

def generate_emergency_story(winning_theme, mode, episode_num=1):
    print("🚨 Avtonom kinematik dvigatel ishga tushdi...")
    seed = random.randint(100, 999)

    hooks = [
        "At 36,000 feet inside the Mariana Trench, the submarine's thermal cameras detected a creature larger than a battleship.",
        "Declassified audio logs confirm the underwater expedition did not disappear from pressure.",
        "Our deep-sea floodlights hit something ancient sleeping on the ocean floor... and it opened its eyes."
    ]

    selected_hook = random.choice(hooks)
    script = (
        f"{selected_hook} Visual sensors locked onto an impossible silhouette moving against the ocean currents. "
        f"The sonar operator reported high-frequency acoustic clicks that shattered the submersible's external hull microphones. "
        f"When primary spotlights were turned to maximum intensity, the entire trench floor shifted. "
        f"It was not a seafloor at all—it was the coiled body of a colossal predatory leviathan. "
        f"The research crew initiated emergency ballast blow, but shadows in the deep move faster than titanium can ascend."
    )

    aspect = "16:9" if mode in ["long_3min", "series_4min", "post"] else "9:16"
    horror_prompts = [
        f"{aspect} photorealistic 8k terrifying gigantic deep sea leviathan serpent opening massive jaws, diver headlight illuminating sharp teeth, dark abyss, Unreal Engine 5",
        f"{aspect} photorealistic 8k gigantic ancient squid monster tentacles wrapping around military submarine, underwater emergency red lights, hyperdetailed cinematic horror",
        f"{aspect} photorealistic 8k deep ocean exploration diver hovering in black water looking at massive glowing bioluminescent eyes in Mariana trench, 8k",
        f"{aspect} photorealistic 8k monstrous abyssal predator with needle teeth lunging toward underwater camera, volumetric blue underwater lights, Octane render"
    ]

    scenes_count = 12 if mode == "shorts" else (36 if mode == "long_3min" else 48)
    sentences = [s.strip() for s in script.split(".") if len(s.strip()) > 5]

    scenes = []
    for i in range(scenes_count):
        txt = sentences[i % len(sentences)]
        p = horror_prompts[i % len(horror_prompts)]
        scenes.append({"text": txt, "prompt": p})

    title = f"What Lurks At 36,000 Feet Below 🌊 #Shorts"
    if mode == "series_4min":
        title = f"ABYSS ARCHIVES - Episode {episode_num}: The Trench Leviathan"
    elif mode == "long_3min":
        title = f"The Unexplained Pacific Trench Breach #{seed}"

    return {
        "title": title,
        "hook": selected_hook,
        "script": script,
        "scenes": scenes,
        "text": f"Expedition Log #{seed}: Deep sonar breach detected. What is guarding the abyss?"
    }

def get_unique_story(winning_theme, past_titles=None, past_hooks=None, mode="shorts", episode_num=1):
    past_titles = past_titles or []
    past_hooks = past_hooks or []

    prompt = build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num)

    result = fetch_internet_ai(prompt)
    if result:
        try:
            return validate_story(result, mode)
        except Exception:
            pass

    fallback_data = generate_emergency_story(winning_theme, mode, episode_num)
    return validate_story(fallback_data, mode)
