import os
import json
import time
import re
import requests
from google import genai


def clean_url(url_str):
    """Har qanday markdown, qavs va ortiqcha belgilarni tozalab, sof URL ajratadi"""
    match = re.search(r'https?://[^\s\)\]\"\']+', url_str)
    if match:
        return match.group(0)
    return url_str.strip()


def clean_json_response(raw_text):
    text = (raw_text or "").strip()
    if not text:
        raise ValueError("Bo'sh AI javobi")

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text, re.S)
        if match:
            return json.loads(match.group(0))
        raise


def build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num=1):
    past_titles_str = "\n- ".join(past_titles[-15:]) if past_titles else "None yet"
    past_hooks_str = "\n- ".join(past_hooks[-15:]) if past_hooks else "None yet"

    if mode == "series_4min":
        return (
            f"You are a top-tier documentary filmmaker directing an episodic deep-sea military thriller.\n"
            f"Write EPISODE {episode_num} of an ongoing series (strictly 4 minutes spoken pace, ~520 words).\n"
            f"Context: '{winning_theme}'.\n"
            "RULES:\n"
            "1. NO CLICHES. Start with unexpected military telemetry or radio distress.\n"
            f"2. FORBIDDEN TITLES:\n- {past_titles_str}\n"
            f"3. FORBIDDEN HOOKS:\n- {past_hooks_str}\n"
            f"4. Title MUST include 'Episode {episode_num}: [Mystery Title]'.\n"
            "5. End with an unresolved chilling cliffhanger.\n"
            "6. Provide EXACTLY 48 scenes.\n"
            "Return ONLY raw valid JSON:\n"
            "{\n"
            f'  "title": "ABYSS ARCHIVES - Episode {episode_num}: Title Under 70 Chars",\n'
            '  "hook": "first spoken sentence",\n'
            '  "script": "Full narration script (~520 words)",\n'
            '  "scenes": [\n'
            '     {"text": "spoken line", "prompt": "16:9 photorealistic 8k dark cinematic deep ocean expedition horror scene, Unreal Engine 5"}\n'
            "  ]\n"
            "}\n"
        )

    elif mode == "long_3min":
        return (
            "You are an elite documentary director. Write an intense 3-minute standalone horizontal military naval mystery (~400 words).\n"
            f"Context: '{winning_theme}'.\n"
            "RULES:\n"
            "1. NO CLICHES.\n"
            f"2. FORBIDDEN TITLES:\n- {past_titles_str}\n"
            f"3. FORBIDDEN HOOKS:\n- {past_hooks_str}\n"
            "4. Divide into EXACTLY 36 scenes.\n"
            "Return ONLY raw valid JSON:\n"
            "{\n"
            '  "title": "Compelling horizontal documentary title (under 70 chars)",\n'
            '  "hook": "first intense spoken sentence",\n'
            '  "script": "Full spoken narrative script (~400 words)",\n'
            '  "scenes": [\n'
            '     {"text": "spoken line", "prompt": "16:9 photorealistic 8k dark cinematic deep ocean naval disaster scene, Unreal Engine 5"}\n'
            "  ]\n"
            "}\n"
        )

    elif mode == "post":
        return (
            "Create an intriguing Community Post update for a deep ocean mystery YouTube channel.\n"
            "Return ONLY raw valid JSON:\n"
            "{\n"
            '  "title": "Community Post Update",\n'
            '  "text": "Intriguing declassified expedition report update ending with a question (~60-80 words).",\n'
            '  "image_prompt": "16:9 cinematic classified black and white polaroid photograph of underwater expedition in dark ocean, 8k"\n'
            "}\n"
        )

    else:
        return (
            "Write an intense US naval abyss horror story (50 seconds spoken pace, ~120 words).\n"
            f"Context: '{winning_theme}'.\n"
            "RULES:\n"
            "1. NO CLICHES.\n"
            f"2. FORBIDDEN TITLES:\n- {past_titles_str}\n"
            f"3. FORBIDDEN HOOKS:\n- {past_hooks_str}\n"
            "4. Divide into EXACTLY 12 scenes.\n"
            "Return ONLY raw valid JSON:\n"
            "{\n"
            '  "title": "punchy title with emoji and #Shorts",\n'
            '  "hook": "first 10 spoken words",\n'
            '  "script": "Full narrative script (~120 words)",\n'
            '  "scenes": [\n'
            '     {"text": "spoken line", "prompt": "vertical 9:16 photorealistic 8k dark underwater cinematic horror prompt"}\n'
            "  ]\n"
            "}\n"
        )


def _gemini_models():
    models = []
    env_model = os.environ.get("GEMINI_MODEL")
    if env_model:
        models.append(env_model.strip())
    models.extend([
        "gemini-2.0-flash",
        "gemini-1.5-flash",
    ])
    seen = set()
    result = []
    for m in models:
        if m and m not in seen:
            seen.add(m)
            result.append(m)
    return result


def _groq_models():
    models = []
    env_model = os.environ.get("GROQ_MODEL")
    if env_model:
        models.append(env_model.strip())
    models.extend([
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
    ])
    seen = set()
    result = []
    for m in models:
        if m and m not in seen:
            seen.add(m)
            result.append(m)
    return result


def get_unique_story(winning_theme, past_titles, past_hooks, mode="shorts", episode_num=1):
    prompt = build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num)

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            client = genai.Client(api_key=gemini_key.strip())
            gemini_models = _gemini_models()
            for attempt, model_name in enumerate(gemini_models, start=1):
                try:
                    print(f"🧠 Gemini urinish {attempt}/{len(gemini_models)} ({model_name})...")
                    res = client.models.generate_content(model=model_name, contents=prompt)
                    text = getattr(res, "text", None)
                    if text:
                        return clean_json_response(text)
                    if hasattr(res, "candidates"):
                        for candidate in res.candidates:
                            content = getattr(candidate, "content", None)
                            if content is None:
                                continue
                            parts = getattr(content, "parts", None)
                            if not parts:
                                continue
                            joined = "".join(getattr(p, "text", "") for p in parts if getattr(p, "text", None))
                            if joined:
                                return clean_json_response(joined)
                except Exception as ge:
                    print(f"⚠️ Gemini ({model_name}) xato: {ge}")
                    if attempt < len(gemini_models):
                        time.sleep(5)
        except Exception as e:
            print(f"⚠️ Gemini konfiguratsiya xatosi: {e}")

    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        groq_url = clean_url("[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)")
        headers = {
            "Authorization": f"Bearer {groq_key.strip()}",
            "Content-Type": "application/json",
        }

        for model_name in _groq_models():
            try:
                print(f"🧠 Groq ({model_name}) ishga tushdi...")
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": "Return only valid JSON. Do not add explanation."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                }
                r = requests.post(groq_url, headers=headers, json=payload, timeout=60)
                print(f"⚠️ Groq ({model_name}) status: {r.status_code}")
                if r.status_code == 200:
                    data = r.json()
                    if "choices" in data and data["choices"]:
                        content = data["choices"][0]["message"]["content"]
                        return clean_json_response(content)
                else:
                    try:
                        print(r.text[:500])
                    except Exception:
                        pass
            except Exception as e:
                print(f"⚠️ Groq ({model_name}) xatoligi: {e}")

    print("🧠 Zaxira AI ishga tushdi...")
    try:
        poll_url = clean_url("[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)")
        payload = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": "You are a JSON generator. Return only raw valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }
        pr = requests.post(poll_url, json=payload, timeout=60)
        print(f"⚠️ Pollinations status: {pr.status_code}")
        if pr.status_code == 200:
            data = pr.json()
            if "choices" in data and data["choices"]:
                content = data["choices"][0]["message"]["content"]
                return clean_json_response(content)
        else:
            try:
                print(pr.text[:500])
            except Exception:
                pass
    except Exception as pe:
        print(f"⚠️ Zaxira AI xatoligi: {pe}")

    raise RuntimeError("Birorta ham AI javob bermadi!")
