import os
import json
import random
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HISTORY_FILE = "history.json"

COUNTRY_REGIONS_DATABASE = [
    {
        "country": "Switzerland",
        "spots": [
            {
                "theme": "Lauterbrunnen & Staubbach Waterfalls",
                "title": "Switzerland – The Valley of 72 Waterfalls (4K)",
                "description": "Emerald vertical cliffs, misting glacial waterfalls, and quiet wooden chalets. #switzerland #nature #travel",
                "queries": [
                    "Lauterbrunnen valley waterfall mist 4k",
                    "Staubbach falls green cliff aerial",
                    "Swiss alps wooden village drone 4k",
                    "Alpine green meadow wildflowers mountains",
                    "Swiss mountain foggy morning valley",
                    "Lauterbrunnen river flowing rocky stream"
                ]
            },
            {
                "theme": "Matterhorn Peak & Zermatt Glaciers",
                "title": "Switzerland – Whispers of the Matterhorn (4K)",
                "description": "Iconic sharp rocky peaks, crystalline alpine reflections, and mountain railways. #matterhorn #switzerland #alps",
                "queries": [
                    "Matterhorn reflection lake Riffelsee 4k",
                    "Zermatt glacier mountain peak cinematic",
                    "Swiss red train snow mountains pass",
                    "Gornergrat panoramic alps drone 4k",
                    "Alpine golden hour sunset mountain ridges",
                    "Misty pine forest swiss high mountains"
                ]
            },
            {
                "theme": "Lake Oeschinen & Blausee Blue Waters",
                "title": "Switzerland – The Secret Turquoise Waters (4K)",
                "description": "Glacial deep turquoise lakes tucked inside massive towering cliff walls. #nature #lakes #aesthetic",
                "queries": [
                    "Oeschinensee turquoise lake drone 4k",
                    "Blausee crystal clear blue water underwater",
                    "Wooden boat floating turquoise alpine lake",
                    "Massive vertical limestone cliff lake reflection",
                    "Swiss pine forest misty lake shore aerial",
                    "Alpine emerald lagoon cinematic 4k"
                ]
            }
        ]
    },
    {
        "country": "Norway",
        "spots": [
            {
                "theme": "Lofoten Islands & Arctic Beaches",
                "title": "Norway – Jagged Peaks of the Arctic Sea (4K)",
                "description": "Dramatic granite walls rising straight out of turquoise Arctic waters. #norway #lofoten #travel",
                "queries": [
                    "Lofoten islands Reine drone 4k",
                    "Hamnoy red fishermen cabins fjord reflection",
                    "Arctic ocean waves crashing dark rocks slow motion",
                    "Lofoten misty mountain road aerial 4k",
                    "Midnight sun norway coastal cliffs",
                    "Nordic fishing village sea fog morning"
                ]
            },
            {
                "theme": "Geirangerfjord & Seven Sisters Falls",
                "title": "Norway – Silence of the Deep Fjords (4K)",
                "description": "Vertical rock walls carving deep blue waters with endless tumbling waterfalls. #fjords #norway #nature",
                "queries": [
                    "Geirangerfjord aerial landscape drone 4k",
                    "Seven sisters waterfall Norway cliff",
                    "Deep blue fjord calm water mountain reflection",
                    "Norwegian fjord viewpoint edge clouds",
                    "Misty green canyon river Norway rapids",
                    "Nordic clouds rolling mountain peak fjord"
                ]
            }
        ]
    },
    {
        "country": "Iceland",
        "spots": [
            {
                "theme": "South Coast Black Sand & Skogafoss",
                "title": "Iceland – Realm of Black Sands and Mist (4K)",
                "description": "Roaring North Atlantic swells meeting pitch-black volcanic sands and basalt pillars. #iceland #nature",
                "queries": [
                    "Reynisfjara black sand beach waves 4k",
                    "Skogafoss massive waterfall rainbow drone",
                    "Seljalandsfoss waterfall behind water stream",
                    "Dyrholaey sea arch cliff aerial 4k",
                    "Basalt columns cave ocean cinematic",
                    "Moody misty volcanic coastline slow motion"
                ]
            },
            {
                "theme": "Glacial Lagoons & Mossy Canyons",
                "title": "Iceland – Floating Ice and Emerald Chasms (4K)",
                "description": "Luminous blue icebergs drifting silently towards black volcanic shores. #iceland #glacier #earth",
                "queries": [
                    "Jokulsarlon glacier lagoon floating ice 4k",
                    "Diamond beach clear ice black sand waves",
                    "Fjadrarargljufur green canyon river drone",
                    "Iceland green moss lava field aerial",
                    "Vatnajokull glacier blue ice cave cinematic",
                    "Iceland volcanic braided river patterns 4k"
                ]
            }
        ]
    },
    {
        "country": "Japan",
        "spots": [
            {
                "theme": "Kyoto Bamboo Groves & Shrines",
                "title": "Japan – Sacred Groves and Timeless Shinto (4K)",
                "description": "Whispering green bamboo forests and serene ancient temple gardens. #japan #aesthetic #peaceful",
                "queries": [
                    "Arashiyama bamboo grove path sunbeams 4k",
                    "Kyoto wooden temple rain zen garden",
                    "Japanese garden koi pond clear water",
                    "Misty mossy forest stone lantern shrine",
                    "Fushimi Inari red torii gates path forest",
                    "Bamboo water fountain garden slow motion"
                ]
            },
            {
                "theme": "Mount Fuji & Five Mirror Lakes",
                "title": "Japan – The Serene Spirit of Mount Fuji (4K)",
                "description": "Pristine reflections of Mount Fuji's snow peak in silent morning mountain lakes. #fuji #japan #nature",
                "queries": [
                    "Mount Fuji sunrise reflection lake 4k drone",
                    "Chureito pagoda view Mount Fuji aerial",
                    "Lake Kawaguchiko misty morning landscape 4k",
                    "Cherry blossoms falling near mountain lake shore",
                    "Mount Fuji dramatic clouds rolling over peak",
                    "Pine trees misty mountain lake sunrise Japan"
                ]
            }
        ]
    }
]

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def get_daily_content_plan():
    history = load_history()
    
    last_country = history[-1].get("country", "") if history else ""
    used_themes = [h.get("theme", "") for h in history if isinstance(h, dict) and "theme" in h]
    used_themes_str = ", ".join(used_themes[-30:]) if used_themes else "None"

    # Ketma-ket bitta davlat tushmasligi uchun davlatni almashtirish
    available_countries = [c for c in COUNTRY_REGIONS_DATABASE if c["country"] != last_country]
    chosen_country_data = random.choice(available_countries if available_countries else COUNTRY_REGIONS_DATABASE)
    country_name = chosen_country_data["country"]

    # Agar GEMINI_API_KEY bo'lsa, o'sha davlatning mutlaqo yangi joyini AI topadi
    if GEMINI_API_KEY:
        prompt = f"""
You are an elite cinematic nature filmmaker.
Generate a video plan for the country: "{country_name}".

STRICT REQUIREMENT:
Do NOT repeat any of these specific places or themes: [{used_themes_str}].
Find a COMPLETELY DIFFERENT region, lake, waterfall, valley, or national park inside {country_name}.

Generate 6 very specific visual queries for Pexels 4K landscape footage.

Return ONLY a valid raw JSON object (no markdown, no backticks):
{{
    "country": "{country_name}",
    "theme": "Specific new place name or region",
    "title": "US Audience Click-Worthy 4K YouTube Title",
    "description": "Poetic 2-sentence description with top hashtags",
    "queries": [
        "precise landscape query 1 4k",
        "water/reflection/waterfall query 2 4k",
        "misty mountain/drone query 3 4k",
        "wide epic nature view 4 4k",
        "dramatic lighting golden hour 5 4k",
        "peaceful aesthetic nature detail 6 4k"
    ]
}}
"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=25)
            raw = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            if raw.startswith("```json"): raw = raw[7:]
            if raw.startswith("```"): raw = raw[3:]
            if raw.endswith("```"): raw = raw[:-3]
            plan = json.loads(raw.strip())
            save_history({"country": plan["country"], "theme": plan["theme"], "title": plan["title"]})
            print(f"[AI TANLOV]: {plan['country']} -> {plan['theme']}")
            return plan
        except Exception:
            pass

    # Zaxira bazadan hali ishlatilmagan yangi lokatsiyani tanlash
    spots = chosen_country_data["spots"]
    unused_spots = [s for s in spots if s["theme"] not in used_themes]
    selected_spot = random.choice(unused_spots) if unused_spots else random.choice(spots)

    plan = {
        "country": country_name,
        "theme": selected_spot["theme"],
        "title": selected_spot["title"],
        "description": selected_spot["description"],
        "queries": selected_spot["queries"]
    }
    save_history({"country": plan["country"], "theme": plan["theme"], "title": plan["title"]})
    print(f"[ZAXIRA TANLOV]: {country_name} -> {plan['theme']}")
    return plan

if __name__ == "__main__":
    print(json.dumps(get_daily_content_plan(), indent=2))
