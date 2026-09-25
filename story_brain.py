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

    # Yedek doğrudan GET motoru
    try:
        get_url = clean_url(f"[https://text.pollinations.ai/](https://text.pollinations.ai/){requests.utils.quote(prompt)}?json=true")
        r = requests.get(get_url, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200 and r.text:
            return clean_json_response(r.text)
    except Exception:
        pass

    return None

# ============================================================
# ÇEVRİMDIŞI 40 YILLIK TÜKENMEZ JENERATÖR
# ============================================================

def generate_emergency_story(mode, past_titles, past_hooks, episode_num=1):
    print("🚨 40 yıllık kombinatorik dinamik kurgu motoru devrede...")

    loc = random.choice(LOCATIONS)
    vessel = random.choice(VESSELS)
    creature = random.choice(CREATURES)
    evt = random.choice(EVENTS)
    climax = random.choice(CLIMAXES)
    
    depth = random.randint(15, 38)
    file_code = f"NAV-LOG-{random.randint(100, 999)}-{chr(random.randint(65, 90))}"

    hooks = [
        f"At {depth},000 feet beneath {loc}, {vessel} intercepted an impossible biological heartbeat.",
        f"Declassified military black boxes confirm {vessel} was dragged downward into {loc}.",
        f"Hydrophone Station Echo registered catastrophic titanium collapse in {loc} right after this sound was logged.",
        f"Telemetry recovered from {vessel} reveals something ancient was disturbed at {depth},000 feet."
    ]

    selected_hook = hooks[0]
    for h in hooks:
        if h not in past_hooks:
            selected_hook = h
            break

    script = (
        f"{selected_hook} "
        f"Emergency sensors indicated that {evt}. "
        f"The recovered acoustic telemetry confirmed {creature} was circling the expedition hull in absolute darkness. "
        f"When secondary high-output floodlights pierced the abyssal water, the crew realized the seafloor was rising beneath them. "
        f"{climax} "
        f"Naval command sealed telemetry file {file_code} under permanent classification protocol."
    )

    aspect = "16:9" if mode in ["long_3min", "series_4min", "post"] else "9:16"
    prompts_pool = [
        f"{aspect} photorealistic 8k terrifying colossal {creature} lunging toward {vessel} searchlights in dark abyss, murky underwater fog, Unreal Engine 5",
        f"{aspect} photorealistic 8k massive ancient sea leviathan jaws closing over submarine in {loc}, emergency red warning beacons, Octane render",
        f"{aspect} photorealistic 8k deep sea exploration diver floating into pitch black trench looking directly into glowing titan eyes, hyperdetailed",
        f"{aspect} photorealistic 8k crushed titanium wreckage of {vessel} surrounded by bioluminescent horrors on ocean floor, cinematic horror"
    ]

    target_count = 12 if mode == "shorts" else (36 if mode == "long_3min" else 48)
    sentences = [s.strip() for s in script.split(".") if len(s.strip()) > 4]

    scenes = []
    for i in range(target_count):
        txt = sentences[i % len(sentences)]
        p = prompts_pool[i % len(prompts_pool)]
        scenes.append({"text": txt, "prompt": p})

    titles = [
        f"What Sank {vessel}? #{random.randint(10, 999)} #Shorts",
        f"The {loc.split('inside')[0].split('at')[0].strip()} Breach #Shorts",
        f"Do Not Dive Into {loc.split('beneath')[0].strip()} 🌊 #Shorts",
        f"Classified Contact At {depth},000 Feet Below #Shorts"
    ]

    selected_title = titles[0]
    for t in titles:
        if t not in past_titles:
            selected_title = t
            break

    if mode == "series_4min":
        selected_title = f"ABYSS ARCHIVES - Episode {episode_num}: The {loc.split('at')[0].strip()}"
    elif mode == "long_3min":
        selected_title = f"Declassified: The Last Dive of {vessel} in {loc.split('inside')[0].strip()}"

    return {
        "title": selected_title,
        "hook": selected_hook,
        "script": script,
        "scenes": scenes,
        "text": f"Incident Record {file_code}: Contact terminated in {loc}. What truly controls the abyss?"
    }

def get_unique_story(winning_theme, past_titles=None, past_hooks=None, mode="shorts", episode_num=1):
    past_titles = past_titles or []
    past_hooks = past_hooks or []

    prompt = build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num)

    # 1. Çoklu internet AI rotalarını dene
    result = fetch_internet_ai(prompt)
    if result:
        try:
            valid_data = validate_story(result, mode)
            if valid_data["title"] not in past_titles and valid_data["hook"] not in past_hooks:
                print("✅ İnternet AI üzerinden özgün, benzersiz senaryo alındı.")
                return valid_data
        except Exception:
            pass

    # 2. İnternet kesilse bile milyonlarca permütasyona sahip dinamik yedek motor
    fallback_data = generate_emergency_story(mode, past_titles, past_hooks, episode_num)
    return validate_story(fallback_data, mode)
