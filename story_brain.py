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
        raise ValueError("Metinde { bulunamadı")

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

    raise ValueError("Eksiksiz JSON bloğu bulunamadı")

def clean_json_response(raw_text):
    if not raw_text:
        raise ValueError("AI boş yanıt döndürdü.")

    text = str(raw_text).strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text).strip()

    json_candidate = extract_valid_json(text)
    data = json.loads(json_candidate)

    if not isinstance(data, dict):
        raise ValueError("Yanıt geçerli bir JSON nesnesi değil.")
    return data

# ============================================================
# 40 YILLIK TÜKENMEZ MATRİS HAVUZU (Milyonlarca Kombinasyon)
# ============================================================

LOCATIONS = [
    "the Challenger Deep inside the Mariana Trench",
    "the abyssal hydrothermal fracture of the Puerto Rico Trench",
    "the submerged spacecraft graveyard of Point Nemo",
    "the magnetic disturbance zone of the Romanche Trench",
    "the ice-shelf subglacial cavern beneath Lake Vostok",
    "the volcanic seafloor canyon of the Kuril-Kamchatka Trench",
    "the declassified nuclear disaster zone of Soviet submarine K-129",
    "the midnight abyss of the Java Sunda Trench",
    "the South Sandwich Trench near the Antarctic perimeter",
    "the unexplored tectonic rift of the Kermadec Trench",
    "the sunken volcanic plateau of the Bermuda Abyssal Plain",
    "the methane hydrate fields off the coast of Svalbard",
    "the Molloy Deep under Arctic ice sheets",
    "the Yap Trench abyssal fault line",
    "the Diamantina Fracture Zone in the South Indian Basin",
    "the Philippine Trench seabed fissure at 34,000 feet",
    "the Aleutian Trench subduction cavern system",
    "the submerged ruins of the Yonaguni tectonic shelf",
    "the dead-zone perimeter of the Baltic Sea Anomaly",
    "the hydrothermal chimney forest of the Guaymas Basin"
]

VESSELS = [
    "US Navy Nuclear Submarine SSN-711",
    "Deep-sea Research Bathyscaphe Proteus-IV",
    "Classified NATO Sonar Surveillance Platform Titan-Echo",
    "Autonomous Abyssal Glider Drone Deep-Scan 9",
    "Submersible Excavation Platform Erebus-3",
    "US Naval Oceanographic Vessel Pathfinder Delta",
    "Soviet-era Titanium Submersible Mir-Omega",
    "Deep Trench Reconnaissance Sub Pioneer-7",
    "Classified DARPA Undersea Habitat Station Alpha-Null",
    "Heavy Seafloor Drilling Crawler Behemoth-2"
]

CREATURES = [
    "an armored serpent-like leviathan spanning over two hundred feet",
    "a colossal ancient cephalopod with bioluminescent crimson eyes",
    "a blind abyssal apex predator with needle-sharp titanium-crushing teeth",
    "a bio-metallic siphonophore entity radiating sonic EMP pulses",
    "a burrowing tectonic worm carving paths through volcanic magma veins",
    "a translucent chitin-plated horror with razor tentacles",
    "an ancient deep-ocean leviathan sleeping in hydrothermal vents",
    "a parasitic abyssal organism capable of fusing with submarine electronics",
    "a gargantuan abyssal angler with bioluminescent hypnotic lures",
    "a segmented armored horror moving at fifty knots along the seafloor"
]

EVENTS = [
    "hull pressure gauges spiked forty percent beyond titanium crush limits",
    "the main propulsion shafts were seized by dense bioluminescent coils",
    "a sustained 14-hertz biological shockwave shattered the forward observation dome",
    "external quartz floodlights revealed massive claw scars tearing the outer plating",
    "all navigation compasses spun erratically before navigation telemetry went black",
    "hydrophones recorded acoustic rhythmic clicks resembling a massive hunting lung",
    "radiation warning systems activated as the sea temperature spiked fifty degrees",
    "the emergency ballast tanks were severed from outside by razor-sharp mandibles"
]

CLIMAXES = [
    "When maximum emergency spotlights ignited, the entire trench floor began moving upward.",
    "A final distorted voice transmission confirmed: 'It is not an anomaly... it is hunting our engines.'",
    "The rescue submersible discovered only shredded hull sections covered in acid residue.",
    "The emergency transponder signal abruptly descended into the earth crust at eighty knots.",
    "Sonar feeds caught the outline of an eye twice the size of the submarine hull opening in the dark.",
    "The black box recording terminated as thousands of glowing tendrils encircled the control room."
]

def build_prompt(mode, winning_theme, past_titles=None, past_hooks=None, episode_num=1):
    past_titles_str = "\n- ".join(past_titles[-30:]) if past_titles else "None"
    past_hooks_str = "\n- ".join(past_hooks[-30:]) if past_hooks else "None"

    # DASHBOARD BUYRUQLARINI O'QISH
    user_cfg_path = os.path.join(os.path.dirname(__file__), "user_instructions.json")
    user_guide = ""
    if os.path.exists(user_cfg_path):
        try:
            with open(user_cfg_path, "r", encoding="utf-8") as f:
                u_data = json.load(f)
                custom_req = u_data.get("custom_prompt", "")
                focus_target = u_data.get("target_focus", "")
                prohibited = u_data.get("prohibited_topics", "")
                horror_lvl = u_data.get("horror_level", "")
                user_guide = (
                    f"\nCREATOR SPECIAL OVERRIDE INSTRUCTIONS:\n"
                    f"- Main Theme Focus: {focus_target}\n"
                    f"- Custom Direction: {custom_req}\n"
                    f"- Horror Atmosphere: {horror_lvl}\n"
                    f"- FORBIDDEN ELEMENTS (STRICTLY AVOID): {prohibited}\n"
                )
        except Exception:
            pass

    loc = random.choice(LOCATIONS)
    vessel = random.choice(VESSELS)
    creature = random.choice(CREATURES)
    evt = random.choice(EVENTS)

    target_words = 120 if mode == "shorts" else (400 if mode == "long_3min" else 520)
    target_scenes = 12 if mode == "shorts" else (36 if mode == "long_3min" else 48)
    aspect = "16:9" if mode in ["long_3min", "series_4min", "post"] else "9:16"

    return f"""
You are a premier documentary filmmaker creating an elite deep-sea naval mystery.
Write a 100% UNIQUE narrative based on:
- Location: {loc}
- Vessel: {vessel}
- Incident: {evt}
- Entity: {creature}
{user_guide}
CRITICAL RULES (ABSOLUTE ZERO REPETITION):
1. Never start with "At 36,000 feet" or generic phrases.
2. Begin immediately with military radio distress, timestamped logs, or anomalous telemetry.
3. FORBIDDEN TITLES:
{past_titles_str}
4. FORBIDDEN HOOKS:
{past_hooks_str}
5. Exact spoken script: ~{target_words} words.
6. EXACTLY {target_scenes} scenes with spoken lines and vivid prompts.

JSON SCHEMA:
{{
  "title": "Shocking High-CTR Title #Shorts",
  "hook": "Unforgettable first sentence",
  "script": "Full narrative script...",
  "scenes": [
    {{"text": "Spoken line", "prompt": "{aspect} photorealistic 8k terrifying {creature} attacking {vessel} in dark abyss, diver floodlights, Unreal Engine 5"}}
  ]
}}
"""

def validate_story(data, mode):
    if not isinstance(data, dict):
        raise ValueError("Sonuç geçerli bir JSON değil.")

    title_val = data.get("title") or data.get("video_title") or f"THE ABYSS ANOMALY #{random.randint(1000, 99999)} #Shorts"
    data["title"] = str(title_val)

    script_val = data.get("script") or data.get("narration") or data.get("story")
    if not script_val:
        raise ValueError("Script metni bulunamadı.")
    data["script"] = str(script_val)

    hook_val = data.get("hook") or data["script"].split(".")[0]
    data["hook"] = str(hook_val)

    scenes = data.get("scenes") or data.get("shots") or []
    target_count = 12 if mode == "shorts" else (36 if mode == "long_3min" else 48)
    aspect = "16:9" if mode in ["long_3min", "series_4min", "post"] else "9:16"

    if not isinstance(scenes, list) or len(scenes) == 0:
        sentences = [s.strip() for s in data["script"].split(".") if len(s.strip()) > 3]
        scenes = []
        for i in range(target_count):
            txt = sentences[i % len(sentences)] if sentences else "The seismic signals accelerated deeper."
            scenes.append({
                "text": txt,
                "prompt": f"{aspect} photorealistic 8k colossal deep sea leviathan mouth opening in pitch black ocean trench, volumetric headlights, Unreal Engine 5"
            })

    for i, sc in enumerate(scenes):
        if isinstance(sc, dict):
            sc.setdefault("text", "The hydrophone sensors continued pulsing.")
            p = sc.get("prompt", "")
            if len(p) < 25 or "ocean" not in p.lower():
                sc["prompt"] = f"{aspect} photorealistic 8k terrifying deep ocean monster emerging from abyssal darkness, diver flashlight beam, Unreal Engine 5"

    data["scenes"] = scenes
    return data

# ============================================================
# İNTERNETTEN AÇIK VE ÜCRETSİZ AI MOTORLARI
# ============================================================

def fetch_internet_ai(prompt):
    engines = [
        ("[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)", "openai"),
        ("[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)", "mistral"),
        ("[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)", "qwen")
    ]

    for url, model in engines:
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a professional mystery scriptwriter. Return only pure JSON."},
                    {"role": "user", "content": prompt}
                ]
            }
            r = requests.post(clean_url(url), json=payload, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                res_data = r.json()
                if "choices" in res_data and len(res_data["choices"]) > 0:
                    content = res_data["choices"][0].get("message", {}).get("content", "")
                    if content:
                        return clean_json_response(content)
        except Exception:
            continue

    try:
        get_url = clean_url(f"[https://text.pollinations.ai/](https://text.pollinations.ai/){requests.
