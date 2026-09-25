# ai_generator.py

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

# Modelni environment orqali o'zgartirish mumkin.
# Masalan:
# set GEMINI_MODEL=gemini-2.5-flash
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

POLLINATIONS_URL = "https://text.pollinations.ai/"

REQUEST_TIMEOUT = 120


# ============================================================
# URL CLEANER
# ============================================================

def clean_url(url_str):
    """
    Markdown URL yoki ortiqcha belgilarni olib tashlaydi.
    """

    if not url_str:
        return ""

    url_str = str(url_str).strip()

    # Markdown:
    # [https://example.com](https://example.com)
    markdown_match = re.search(
        r"\]\((https?://[^)]+)\)",
        url_str
    )

    if markdown_match:
        return markdown_match.group(1)

    # Oddiy URL
    match = re.search(
        r"https?://[^\s\)\]\"']+",
        url_str
    )

    if match:
        return match.group(0)

    return url_str


# ============================================================
# JSON CLEANER
# ============================================================

def clean_json_response(raw_text):
    """
    AI qaytargan javobdan JSON obyektni ajratib oladi.
    Markdown ```json ... ``` ni ham tozalaydi.
    """

    if raw_text is None:
        raise ValueError("AI bo'sh javob qaytardi.")

    text = str(raw_text).strip()

    if not text:
        raise ValueError("AI bo'sh javob qaytardi.")

    # ```json
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # ```
    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    # Oxiridagi ```
    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    # JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:

        print("\n========== JSON XATOSI ==========")
        print("AI javobi:")
        print(text[:2000])
        print("=================================\n")

        raise ValueError(
            f"AI JSON qaytarmadi: {e}"
        )

    if not isinstance(data, dict):
        raise ValueError(
            "AI JSON obyekt emas."
        )

    return data


# ============================================================
# PROMPT
# ============================================================

def build_prompt(
    mode,
    winning_theme,
    past_titles=None,
    past_hooks=None,
    episode_num=1
):

    past_titles = past_titles or []
    past_hooks = past_hooks or []

    past_titles_str = (
        "\n- ".join(past_titles[-15:])
        if past_titles
        else "None yet"
    )

    past_hooks_str = (
        "\n- ".join(past_hooks[-15:])
        if past_hooks
        else "None yet"
    )

    # --------------------------------------------------------
    # 4 MIN SERIES
    # --------------------------------------------------------

    if mode == "series_4min":

        return f"""
You are a top-tier documentary filmmaker creating an episodic
deep-sea military mystery thriller.

Write EPISODE {episode_num}.

Context:
{winning_theme}

TARGET:
Approximately 4 minutes spoken narration.
Approximately 520 words.

RULES:

1. Start immediately with unusual military telemetry,
   sonar data, radio distress, or classified information.

2. NO generic horror clichés.

3. Do not copy previous titles.

FORBIDDEN TITLES:
- {past_titles_str}

4. Do not copy previous hooks.

FORBIDDEN HOOKS:
- {past_hooks_str}

5. Title MUST contain:
Episode {episode_num}:

6. End with an unresolved chilling cliffhanger.

7. EXACTLY 48 scenes.

8. Every scene must contain:
   - text
   - prompt

9. Image prompts must describe cinematic deep-ocean
   military documentary visuals.

10. Return ONLY valid JSON.
DO NOT use Markdown.
DO NOT use ```json.

JSON FORMAT:

{{
    "title": "ABYSS ARCHIVES - Episode {episode_num}: Mystery Title",
    "hook": "First spoken sentence",
    "script": "Full narration script",
    "scenes": [
        {{
            "text": "Spoken line",
            "prompt": "16:9 photorealistic cinematic deep ocean military expedition, dark mysterious underwater environment, realistic submarine, volumetric lighting, ultra detailed, Unreal Engine 5"
        }}
    ]
}}
"""


    # --------------------------------------------------------
    # 3 MIN VIDEO
    # --------------------------------------------------------

    elif mode == "long_3min":

        return f"""
You are an elite documentary filmmaker.

Create an intense 3-minute standalone horizontal
military naval mystery documentary.

Context:
{winning_theme}

TARGET:
Approximately 400 words.

RULES:

1. No cliché opening.

2. Start with something strange:
   military telemetry, sonar, radio transmission,
   classified recording, or unexplained naval event.

3. Avoid these previous titles:

FORBIDDEN TITLES:
- {past_titles_str}

4. Avoid these previous hooks:

FORBIDDEN HOOKS:
- {past_hooks_str}

5. EXACTLY 36 scenes.

6. Every scene must contain:
   text
   prompt

7. Return ONLY raw valid JSON.

JSON FORMAT:

{{
    "title": "Compelling Naval Mystery Documentary",
    "hook": "First intense spoken sentence",
    "script": "Full spoken narrative",
    "scenes": [
        {{
            "text": "Spoken line",
            "prompt": "16:9 photorealistic cinematic deep ocean naval mystery, realistic submarine, dark water, dramatic lighting, ultra detailed, Unreal Engine 5"
        }}
    ]
}}
"""


    # --------------------------------------------------------
    # COMMUNITY POST
    # --------------------------------------------------------

    elif mode == "post":

        return f"""
Create an intriguing Community Post for a deep-ocean
mystery YouTube channel.

Context:
{winning_theme}

Return ONLY valid JSON.

JSON FORMAT:

{{
    "title": "Community Post Update",
    "text": "Intriguing classified expedition report update ending with a question, approximately 60-80 words.",
    "image_prompt": "16:9 cinematic classified underwater expedition photograph, mysterious dark ocean, documentary style, ultra detailed"
}}
"""


    # --------------------------------------------------------
    # SHORTS
    # --------------------------------------------------------

    else:

        return f"""
You are a professional YouTube Shorts documentary writer.

Create an intense 50-second US naval abyss mystery story.

Context:
{winning_theme}

TARGET:
Approximately 120 words.

RULES:

1. NO cliché opening.

2. Start with an unexpected:
   sonar reading, military transmission,
   classified recording, or strange discovery.

3. Avoid previous titles.

FORBIDDEN TITLES:
- {past_titles_str}

4. Avoid previous hooks.

FORBIDDEN HOOKS:
- {past_hooks_str}

5. EXACTLY 12 scenes.

6. Every scene must contain:
   text
   prompt

7. Vertical format:
   9:16

8. Return ONLY valid JSON.

JSON FORMAT:

{{
    "title": "Punchy mystery title #Shorts",
    "hook": "First intense sentence",
    "script": "Full approximately 120 word narration",
    "scenes": [
        {{
            "text": "Spoken line",
            "prompt": "9:16 photorealistic cinematic deep underwater military mystery, dark ocean, submarine, dramatic volumetric lighting, ultra detailed, Unreal Engine 5"
        }}
    ]
}}
"""


# ============================================================
# VALIDATION
# ============================================================

def validate_story(data, mode):

    if not isinstance(data, dict):
        raise ValueError("Natija JSON object emas.")

    required = [
        "title",
        "hook",
        "script"
    ]

    for field in required:

        if field not in data:
            raise ValueError(
                f"JSON ichida '{field}' yo'q."
            )

    if not data["title"]:
        raise ValueError("Title bo'sh.")

    if not data["script"]:
        raise ValueError("Script bo'sh.")

    # Post boshqa format
    if mode == "post":

        if "text" not in data:
            raise ValueError(
                "Post uchun 'text' topilmadi."
            )

        if "image_prompt" not in data:
            raise ValueError(
                "Post uchun 'image_prompt' topilmadi."
            )

        return data

    # Video scenes
    if "scenes" not in data:
        raise ValueError(
            "JSON ichida 'scenes' yo'q."
        )

    scenes = data["scenes"]

    if not isinstance(scenes, list):
        raise ValueError(
            "'scenes' list bo'lishi kerak."
        )

    expected = {
        "shorts": 12,
        "long_3min": 36,
        "series_4min": 48
    }

    if mode in expected:

        required_count = expected[mode]

        if len(scenes) != required_count:

            raise ValueError(
                f"{mode} uchun {required_count} ta scene kerak. "
                f"AI {len(scenes)} ta qaytardi."
            )

    for i, scene in enumerate(scenes, 1):

        if not isinstance(scene, dict):
            raise ValueError(
                f"{i}-scene object emas."
            )

        if "text" not in scene:
            raise ValueError(
                f"{i}-scene text yo'q."
            )

        if "prompt" not in scene:
            raise ValueError(
                f"{i}-scene prompt yo'q."
            )

    return data


# ============================================================
# GEMINI
# ============================================================

def generate_with_gemini(prompt):

    if not GEMINI_API_KEY:

        print("⚠️ GEMINI_API_KEY topilmadi.")

        return None

    if genai is None:

        print(
            "⚠️ google-genai o'rnatilmagan."
        )

        return None

    try:

        print(
            f"🧠 Gemini ({GEMINI_MODEL}) ishga tushmoqda..."
        )

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"   Gemini urinish {attempt}/3..."
                )

                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )

                if response and response.text:

                    print(
                        "✅ Gemini javob berdi."
                    )

                    return clean_json_response(
                        response.text
                    )

            except Exception as e:

                print(
                    f"⚠️ Gemini xatosi: {e}"
                )

                if attempt < 3:
                    time.sleep(3)

    except Exception as e:

        print(
            f"⚠️ Gemini ishga tushmadi: {e}"
        )

    return None


# ============================================================
# POLLINATIONS
# ============================================================

def generate_with_pollinations(prompt):

    print(
        "🧠 Pollinations zaxira AI ishga tushmoqda..."
    )

    try:

        response = requests.post(
            POLLINATIONS_URL,
            params={
                "model": "openai",
                "json": "true"
            },
            data=prompt.encode("utf-8"),
            headers={
                "Content-Type": "text/plain; charset=utf-8"
            },
            timeout=REQUEST_TIMEOUT
        )

        print(
            f"Pollinations HTTP: {response.status_code}"
        )

        if response.status_code != 200:

            print(
                "Pollinations xatosi:"
            )

            print(
                response.text[:1000]
            )

            return None

        if not response.text.strip():

            print(
                "⚠️ Pollinations bo'sh javob berdi."
            )

            return None

        print(
            "✅ Pollinations javob berdi."
        )

        return clean_json_response(
            response.text
        )

    except requests.exceptions.Timeout:

        print(
            "⚠️ Pollinations timeout."
        )

    except requests.exceptions.ConnectionError as e:

        print(
            f"⚠️ Pollinations connection error: {e}"
        )

    except Exception as e:

        print(
            f"⚠️ Pollinations xatosi: {e}"
        )

    return None


# ============================================================
# MAIN GENERATOR
# ============================================================

def get_unique_story(
    winning_theme,
    past_titles=None,
    past_hooks=None,
    mode="shorts",
    episode_num=1
):

    past_titles = past_titles or []
    past_hooks = past_hooks or []

    print("\n")
    print("=" * 60)
    print("🚀 AI STORY GENERATOR")
    print("=" * 60)

    print(
        f"Mode: {mode}"
    )

    print(
        f"Theme: {winning_theme}"
    )

    # Prompt
    prompt = build_prompt(
        mode=mode,
        winning_theme=winning_theme,
        past_titles=past_titles,
        past_hooks=past_hooks,
        episode_num=episode_num
    )

    # --------------------------------------------------------
    # 1. GEMINI
    # --------------------------------------------------------

    result = generate_with_gemini(
        prompt
    )

    if result:

        try:

            result = validate_story(
                result,
                mode
            )

            print(
                "✅ Gemini story VALID."
            )

            return result

        except Exception as e:

            print(
                f"⚠️ Gemini JSON validatsiya xatosi: {e}"
            )

    # --------------------------------------------------------
    # 2. POLLINATIONS
    # --------------------------------------------------------

    result = generate_with_pollinations(
        prompt
    )

    if result:

        try:

            result = validate_story(
                result,
                mode
            )

            print(
                "✅ Pollinations story VALID."
            )

            return result

        except Exception as e:

            print(
                f"⚠️ Pollinations JSON validatsiya xatosi: {e}"
            )

    # --------------------------------------------------------
    # FAILED
    # --------------------------------------------------------

    raise RuntimeError(
        "\n"
        "❌ AI tizimlaridan valid story olib bo'lmadi.\n"
        "\n"
        "Tekshiring:\n"
        "1. GEMINI_API_KEY mavjudmi?\n"
        "2. google-genai o'rnatilganmi?\n"
        "3. Internet ishlayaptimi?\n"
        "4. GEMINI_MODEL to'g'rimi?\n"
        "5. Pollinations API javob beryaptimi?\n"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "AI Generator test boshlandi..."
    )

    try:

        result = get_unique_story(
            winning_theme=(
                "A classified submarine discovered "
                "an impossible sonar signal "
                "deep beneath the Pacific Ocean."
            ),
            past_titles=[],
            past_hooks=[],
            mode="shorts",
            episode_num=1
        )

        print("\n" + "=" * 60)
        print("🎉 NATIJA")
        print("=" * 60)

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )

    except Exception as e:

        print("\n❌ TEST XATOSI:")
        print(e)
