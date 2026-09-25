# ============================================================
# STORY BRAIN
# Gemini + Pollinations
# JSON Schema + Validation + Retry + Fallback
# ============================================================

import os
import json
import time
import re
import random
import requests


# ============================================================
# CONFIG
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.0-flash"
).strip()

POLLINATIONS_API_KEY = os.getenv(
    "POLLINATIONS_API_KEY",
    ""
).strip()

POLLINATIONS_URL = (
    "https://gen.pollinations.ai/v1/chat/completions"
)

POLLINATIONS_MODEL = os.getenv(
    "POLLINATIONS_MODEL",
    "openai"
).strip()

REQUEST_TIMEOUT = 180
MAX_RETRIES = 6


def get_retry_delay(response=None, attempt=1):
    """Use provider retry timing when available; otherwise do exponential backoff."""
    if response is not None:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return max(5, int(float(retry_after)))
            except ValueError:
                pass

    backoff = min(60, 5 * (2 ** max(0, attempt - 1)))
    jitter = random.uniform(0, 4)
    return backoff + jitter


# ============================================================
# DEBUG
# ============================================================

def debug_config():

    print()
    print("=" * 60)
    print("🔧 STORY BRAIN CONFIG")
    print("=" * 60)

    print(
        f"GEMINI_MODEL: {GEMINI_MODEL}"
    )

    print(
        "GEMINI_API_KEY:",
        "YES" if GEMINI_API_KEY else "NO"
    )

    print(
        f"POLLINATIONS_MODEL: {POLLINATIONS_MODEL}"
    )

    print(
        "POLLINATIONS_API_KEY:",
        "YES" if POLLINATIONS_API_KEY else "NO"
    )

    print(
        f"POLLINATIONS_URL: {POLLINATIONS_URL}"
    )

    print("=" * 60)
    print()


# ============================================================
# JSON CLEANER
# ============================================================

def clean_json_response(raw_text):

    if raw_text is None:
        raise ValueError(
            "AI bo'sh javob qaytardi."
        )

    text = str(raw_text).strip()

    if not text:
        raise ValueError(
            "AI bo'sh javob qaytardi."
        )

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "AI javobida JSON object topilmadi."
        )

    text = text[start:end + 1]

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print()
        print("=" * 60)
        print("❌ JSON PARSE ERROR")
        print("=" * 60)
        print(f"Xato: {e}")
        print()
        print("AI javobining boshlanishi:")
        print(text[:3000])
        print("=" * 60)
        raise ValueError(f"JSON parsing xatosi: {e}")

    if not isinstance(data, dict):
        raise ValueError(
            "AI JSON object qaytarmadi."
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
        "\n- ".join(
            str(x) for x in past_titles[-15:]
        )
        if past_titles
        else "None"
    )

    past_hooks_str = (
        "\n- ".join(
            str(x) for x in past_hooks[-15:]
        )
        if past_hooks
        else "None"
    )

    if mode == "series_4min":
        return f"""
You are a professional cinematic documentary writer.

Create EPISODE {episode_num} of an ongoing
deep-ocean mystery documentary series.

THEME:
{winning_theme}

TARGET:
Approximately 520 spoken words.

STRICT REQUIREMENTS:

1. Start with unusual telemetry, sonar,
radio transmission, classified data,
or unexplained discovery.

2. No generic horror clichés.

3. Create an original title.

FORBIDDEN TITLES:
{past_titles_str}

4. Create an original hook.

FORBIDDEN HOOKS:
{past_hooks_str}

5. Title must contain:
Episode {episode_num}:

6. End with an unresolved cliffhanger.

7. EXACTLY 48 scenes.

8. Every scene MUST have:
text
prompt

9. Every prompt must be cinematic,
photorealistic and suitable for image generation.

10. Return ONLY JSON.

NO MARKDOWN.
NO EXPLANATION.
NO ```json.

JSON:
{{
  "title": "ABYSS ARCHIVES - Episode {episode_num}: Mystery Title",
  "hook": "First spoken sentence",
  "script": "Full narration script",
  "scenes": [
    {{
      "text": "Spoken line",
      "prompt": "16:9 photorealistic cinematic deep ocean documentary"
    }}
  ]
}}
"""

    if mode == "long_3min":
        return f"""
You are an elite cinematic documentary writer.

Create an intense 3-minute standalone
deep-ocean mystery documentary.

THEME:
{winning_theme}

TARGET:
Approximately 400 spoken words.

STRICT REQUIREMENTS:

1. Start immediately with something unusual.

2. Use sonar readings, telemetry,
radio transmissions, classified recordings,
or unexplained discoveries.

3. Create a completely original title.

FORBIDDEN TITLES:
{past_titles_str}

4. Create a completely original hook.

FORBIDDEN HOOKS:
{past_hooks_str}

5. EXACTLY 36 scenes.

6. Every scene MUST contain:
text
prompt

7. Video format: 16:9.

8. Return ONLY valid JSON.

NO MARKDOWN.
NO EXPLANATION.
NO ```json.

JSON:
{{
  "title": "Compelling Deep Ocean Mystery",
  "hook": "First intense spoken sentence",
  "script": "Full narration script",
  "scenes": [
    {{
      "text": "Spoken line",
      "prompt": "16:9 photorealistic cinematic deep ocean documentary, realistic submarine, mysterious underwater environment, dramatic lighting, ultra detailed"
    }}
  ]
}}
"""

    if mode == "post":
        return f"""
Create an intriguing YouTube Community Post.

THEME:
{winning_theme}

Write approximately 60-80 words.

End with an interesting question.

Return ONLY valid JSON.

JSON:
{{
  "title": "Community Post Update",
  "text": "Intriguing expedition report ending with a question.",
  "image_prompt": "16:9 cinematic mysterious underwater expedition photograph, documentary style, ultra detailed"
}}
"""

    return f"""
You are a professional YouTube Shorts documentary writer.

Create an intense 50-second deep-ocean mystery story.

THEME:
{winning_theme}

TARGET:
Approximately 120 spoken words.

STRICT REQUIREMENTS:

1. Start with sonar,
radio transmission,
classified recording,
or strange discovery.

2. No cliché opening.

3. Create an original title.

FORBIDDEN TITLES:
{past_titles_str}

4. Create an original hook.

FORBIDDEN HOOKS:
{past_hooks_str}

5. EXACTLY 12 scenes.

6. Every scene MUST contain:
text
prompt

7. Video format: 9:16.

8. Return ONLY valid JSON.

NO MARKDOWN.
NO EXPLANATION.

JSON:
{{
  "title": "Punchy Mystery Title #Shorts",
  "hook": "First intense sentence",
  "script": "Approximately 120 word narration",
  "scenes": [
    {{
      "text": "Spoken line",
      "prompt": "9:16 photorealistic cinematic deep underwater mystery, dark ocean, realistic submarine, dramatic lighting, ultra detailed"
    }}
  ]
}}
"""


# ============================================================
# GEMINI JSON SCHEMA
# ============================================================

def get_gemini_schema(mode):

    if mode == "post":
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "text": {"type": "string"},
                "image_prompt": {"type": "string"}
            },
            "required": ["title", "text", "image_prompt"]
        }

    return {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "hook": {"type": "string"},
            "script": {"type": "string"},
            "scenes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "prompt": {"type": "string"}
                    },
                    "required": ["text", "prompt"]
                }
            }
        },
        "required": ["title", "hook", "script", "scenes"]
    }


# ============================================================
# VALIDATOR
# ============================================================

def validate_story(data, mode):

    if not isinstance(data, dict):
        raise ValueError("Story dict/object emas.")

    if mode == "post":
        required = ["title", "text", "image_prompt"]
        for field in required:
            if field not in data:
                raise ValueError(f"Post '{field}' mavjud emas.")
            if not isinstance(data[field], str):
                raise ValueError(f"Post '{field}' string emas.")
            if not data[field].strip():
                raise ValueError(f"Post '{field}' bo'sh.")
        return data

    required = ["title", "hook", "script", "scenes"]
    for field in required:
        if field not in data:
            raise ValueError(f"Video '{field}' mavjud emas.")

    for field in ["title", "hook", "script"]:
        if not isinstance(data[field], str):
            raise ValueError(f"'{field}' string emas.")
        if not data[field].strip():
            raise ValueError(f"'{field}' bo'sh.")

    scenes = data["scenes"]
    if not isinstance(scenes, list):
        raise ValueError("'scenes' list emas.")

    expected_counts = {
        "shorts": 12,
        "long_3min": 36,
        "series_4min": 48
    }
    expected = expected_counts.get(mode)
    if expected is None:
        raise ValueError(f"Noma'lum mode: {mode}")
    if len(scenes) != expected:
        raise ValueError(f"{mode}: {expected} scene kerak, AI {len(scenes)} ta berdi.")

    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            raise ValueError(f"{index}-scene object emas.")
        if "text" not in scene:
            raise ValueError(f"{index}-scene text yo'q.")
        if "prompt" not in scene:
            raise ValueError(f"{index}-scene prompt yo'q.")
        if not isinstance(scene["text"], str):
            raise ValueError(f"{index}-scene text string emas.")
        if not isinstance(scene["prompt"], str):
            raise ValueError(f"{index}-scene prompt string emas.")
        if not scene["text"].strip():
            raise ValueError(f"{index}-scene text bo'sh.")
        if not scene["prompt"].strip():
            raise ValueError(f"{index}-scene prompt bo'sh.")

    return data


# ============================================================
# GEMINI 2.0/2.5 direct REST API
# ============================================================

def generate_with_gemini(prompt, mode):

    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY mavjud emas.")
        return None

    print()
    print(f"🧠 Gemini {GEMINI_MODEL}")

    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"   Gemini urinish {attempt}/{MAX_RETRIES}")

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )

            print(f"   Gemini HTTP: {response.status_code}")

            if response.status_code == 200:
                api_data = response.json()
                candidate = api_data.get("candidates", [{}])[0]
                content = candidate.get("content", {})
                parts = content.get("parts", [])

                output = ""
                for part in parts:
                    if isinstance(part, dict) and part.get("text"):
                        output = part.get("text")
                        break

                if not output:
                    raise ValueError("Gemini response ichida output_text topilmadi.")

                print("✅ Gemini javob berdi.")
                data = clean_json_response(output)
                validate_story(data, mode)
                print("✅ Gemini JSON + validation OK.")
                return data

            if response.status_code in [408, 429, 500, 502, 503, 504]:
                print("⚠️ Gemini vaqtinchalik xato:")
                print(response.text[:1500])

                if attempt < MAX_RETRIES:
                    wait = get_retry_delay(response, attempt)
                    print(f"   {wait:.1f}s kutamiz...")
                    time.sleep(wait)
                    continue

            print()
            print("❌ GEMINI API ERROR")
            print(response.text[:3000])
            return None

        except requests.exceptions.Timeout:
            print("⚠️ Gemini timeout.")
            if attempt < MAX_RETRIES:
                time.sleep(get_retry_delay(None, attempt))

        except requests.exceptions.ConnectionError as e:
            print("⚠️ Gemini connection error:")
            print(e)
            if attempt < MAX_RETRIES:
                time.sleep(get_retry_delay(None, attempt))

        except Exception as e:
            print("⚠️ Gemini processing error:")
            print(e)
            if attempt < MAX_RETRIES:
                time.sleep(get_retry_delay(None, attempt))

    return None


# ============================================================
# POLLINATIONS
# ============================================================

def generate_with_pollinations(prompt, mode):

    if not POLLINATIONS_API_KEY:
        print()
        print("❌ POLLINATIONS_API_KEY mavjud emas.")
        return None

    print()
    print(f"🌸 Pollinations {POLLINATIONS_MODEL}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {POLLINATIONS_API_KEY}"
    }

    payload = {
        "model": POLLINATIONS_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional cinematic documentary writer. "
                    "Return ONLY valid JSON. Never use Markdown."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"   Pollinations urinish {attempt}/{MAX_RETRIES}")

        try:
            response = requests.post(
                POLLINATIONS_URL,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )

            print(f"   Pollinations HTTP: {response.status_code}")

            if response.status_code == 200:
                api_data = response.json()
                choices = api_data.get("choices", [])
                if not choices:
                    raise ValueError("Pollinations choices yo'q.")

                message = choices[0].get("message", {})
                content = message.get("content", "")

                if isinstance(content, list):
                    parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            parts.append(item.get("text", ""))
                    content = "".join(parts)

                if not content:
                    raise ValueError("Pollinations content bo'sh.")

                print("✅ Pollinations javob berdi.")
                data = clean_json_response(content)
                validate_story(data, mode)
                print("✅ Pollinations JSON + validation OK.")
                return data

            if response.status_code in [408, 429, 500, 502, 503, 504]:
                print("⚠️ Pollinations vaqtinchalik xato:")
                print(response.text[:1500])

                if attempt < MAX_RETRIES:
                    wait = get_retry_delay(response, attempt)
                    print(f"   {wait:.1f}s kutamiz...")
                    time.sleep(wait)
                    continue

            print()
            print("❌ POLLINATIONS API ERROR")
            print(response.text[:3000])
            return None

        except requests.exceptions.Timeout:
            print("⚠️ Pollinations timeout.")
            if attempt < MAX_RETRIES:
                time.sleep(get_retry_delay(None, attempt))

        except requests.exceptions.ConnectionError as e:
            print("⚠️ Pollinations connection error:")
            print(e)
            if attempt < MAX_RETRIES:
                time.sleep(get_retry_delay(None, attempt))

        except Exception as e:
            print("⚠️ Pollinations processing error:")
            print(e)
            if attempt < MAX_RETRIES:
                time.sleep(get_retry_delay(None, attempt))

    return None


# ============================================================
# MAIN STORY FUNCTION
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

    print()
    print("=" * 70)
    print("🚀 AI STORY GENERATOR")
    print("=" * 70)
    print(f"Mode: {mode}")
    print(f"Theme: {winning_theme}")
    print(f"Episode: {episode_num}")

    debug_config()

    prompt = build_prompt(
        mode=mode,
        winning_theme=winning_theme,
        past_titles=past_titles,
        past_hooks=past_hooks,
        episode_num=episode_num
    )

    print()
    print("=" * 70)
    print("1️⃣ GEMINI")
    print("=" * 70)

    result = generate_with_gemini(prompt=prompt, mode=mode)
    if result is not None:
        print()
        print("🎉 GEMINI STORY READY.")
        return result

    print()
    print("=" * 70)
    print("2️⃣ POLLINATIONS FALLBACK")
    print("=" * 70)

    result = generate_with_pollinations(prompt=prompt, mode=mode)
    if result is not None:
        print()
        print("🎉 POLLINATIONS STORY READY.")
        return result

    raise RuntimeError(
        "\n"
        "❌ AI tizimlaridan valid story olib bo'lmadi.\n"
        "\n"
        "Tekshirildi:\n"
        "1. Gemini API\n"
        "2. Gemini JSON schema\n"
        "3. Gemini JSON parsing\n"
        "4. Scene count\n"
        "5. Scene text/prompt\n"
        "6. Pollinations API\n"
        "7. Pollinations JSON parsing\n"
        "8. Pollinations story validation\n"
        "\n"
        f"Mode: {mode}\n"
        f"Gemini model: {GEMINI_MODEL}\n"
        f"Gemini key: {'YES' if GEMINI_API_KEY else 'NO'}\n"
        f"Pollinations model: {POLLINATIONS_MODEL}\n"
        f"Pollinations key: {'YES' if POLLINATIONS_API_KEY else 'NO'}\n"
    )


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("🧪 STORY BRAIN LOCAL TEST")
    print("=" * 70)

    test_theme = (
        "What Lurks at 36,000 Feet Below? "
        "A mysterious deep-ocean discovery."
    )

    try:
        result = get_unique_story(
            winning_theme=test_theme,
            past_titles=[],
            past_hooks=[],
            mode="long_3min",
            episode_num=1
        )

        print()
        print("=" * 70)
        print("🎉 STORY GENERATED SUCCESSFULLY")
        print("=" * 70)

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print()
        print("=" * 70)
        print("❌ FINAL ERROR")
        print("=" * 70)
        print(str(e))
