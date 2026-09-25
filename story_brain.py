import os
import json
import time
import requests
from google import genai

def clean_json_response(raw_text):
    text = raw_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

def build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num=1):
    past_titles_str = "\n- ".join(past_titles[-15:]) if past_titles else "None yet"
    past_hooks_str = "\n- ".join(past_hooks[-15:]) if past_hooks else "None yet"

    if mode == "series_4min":
        return (
            f"You are a top-tier Netflix/HBO investigative horror director creating an episodic deep-sea military series.\n"
            f"Write EPISODE {episode_num} of an ongoing serialized dark ocean expedition documentary (strictly 4 minutes spoken pace, ~520 words).\n"
            f"High-engagement channel context: '{winning_theme}'.\n"
            "STRICT RULES:\n"
            "1. NO CLICHE OPENINGS. Start with sudden high-stakes military telemetry, radio distress, or classified expedition log.\n"
            f"2. FORBIDDEN RECENT TITLES:\n- {past_titles_str}\n"
            f"3. FORBIDDEN OPENING HOOKS:\n- {past_hooks_str}\n"
            f"4. The title MUST include 'Episode {episode_num}: [Compelling Mystery Title]'.\n"
            "5. The ending MUST be a terrifying cliffhanger setting up the next episode with an intense unresolved mystery.\n"
            "6. Split into EXACTLY 48 chronological scenes (5 seconds per scene).\n"
            "Return ONLY raw valid JSON (no markdown, no backticks):\n"
            "{\n"
            f'  "title": "ABYSS ARCHIVES - Episode {episode_num}: Title Under 70 Chars",\n'
            '  "hook": "first chilling spoken sentence",\n'
            '  "script": "Full spoken narrative script (~520 words)",\n'
            '  "scenes": [\n'
            '     {"text": "spoken narration sentence", "prompt": "16:9 photorealistic 8k dark cinematic deep ocean expedition horror scene, Unreal Engine 5, hyper-detailed"}\n'
            "  ]\n"
            "}"
        )

    elif mode == "long_3min":
        return (
            "You are an elite Hollywood mystery-thriller director. Write an intense 3-minute complete standalone horizontal military naval documentary (~400 words).\n"
            f"Context: '{winning_theme}'.\n"
            "STRICT RULES:\n"
            "1. NO CLICHE OPENINGS.\n"
            f"2. FORBIDDEN RECENT TITLES:\n- {past_titles_str}\n"
            f"3. FORBIDDEN OPENING HOOKS:\n- {past_hooks_str}\n"
            "4. Divide into EXACTLY 36 short chronological scenes (5 seconds per scene).\n"
            "Return ONLY raw valid JSON:\n"
            "{\n"
            '  "title": "Compelling horizontal documentary title (under 70 chars)",\n'
            '  "hook": "first intense spoken hook sentence",\n'
            '  "script": "Full narrative script (~400 words)",\n'
            '  "scenes": [\n'
            '     {"text": "spoken sentence", "prompt": "16:9 photorealistic 8k dark cinematic deep ocean naval disaster scene, Unreal Engine 5"}\n'
            "  ]\n"
            "}"
        )

    elif mode == "post":
        return (
            "You are managing a viral mystery & naval horror YouTube channel community tab.\n"
            "Create an intriguing, engaging Community Post question/poll update that hooks the audience about a declassified deep ocean recovery operation.\n"
            "Return ONLY raw valid JSON:\n"
            "{\n"
            '  "title": "Community Post Update",\n'
            '  "text": "Intriguing post text with declassified report vibes, ending with an open question for subscribers (around 60-80 words).",\n'
            '  "image_prompt": "16:9 cinematic classified black and white polaroid recovery photograph of sunken naval equipment in dark waters, mysterious atmosphere, 8k"\n'
            "}"
        )

    else:
        return (
            "You are an elite horror director. Write an intense US naval abyss horror story (50 seconds spoken pace).\n"
            f"Context: '{winning_theme}'.\n"
            "STRICT RULES:\n"
            "1. NO CLICHE OPENINGS.\n"
            f"2. FORBIDDEN RECENT TITLES:\n- {past_titles_str}\n"
            f"3. FORBIDDEN OPENING HOOKS:\n- {past_hooks_str}\n"
            "4. Divide into EXACTLY 12 scenes.\n"
            "Return ONLY raw valid JSON:\n"
            "{\n"
            '  "title": "punchy title with emoji and #Shorts",\n'
            '  "hook": "first 10 spoken words",\n'
            '  "script": "Full narrative script (~120 words)",\n'
            '  "scenes": [\n'
            '     {"text": "spoken line", "prompt": "vertical 9:16 photorealistic 8k dark underwater cinematic horror prompt"}\n'
            "  ]\n"
            "}"
        )

def get_unique_story(winning_theme, past_titles, past_hooks, mode="shorts", episode_num=1):
    prompt = build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num)

    # 1. Gemini (Zaxira modellari bilan birma-bir sinash)
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        client = genai.Client(api_key=gemini_key.strip())
        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        for m in models_to_try:
            try:
                print(f"🧠 Gemini ({m}) ishga tushdi ({mode.upper()})...")
                res = client.models.generate_content(model=m, contents=prompt)
                if res and res.text:
                    return clean_json_response(res.text)
            except Exception as e:
                print(f"⚠️ Gemini ({m}) xatoligi: {e}")
                time.sleep(1)

    # 2. Groq (To'g'rilangan manzili va bepul yuqori tezlik)
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            print(f"🧠 Groq ishga tushdi ({mode.upper()})...")
            url = "[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)"
            headers = {
                "Authorization": f"Bearer {groq_key.strip()}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            if r.status_code == 200:
                data = r.json()
                return json.loads(data["choices"][0]["message"]["content"])
            else:
                print(f"⚠️ Groq xatoligi: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"⚠️ Groq ulanish xatoligi: {e}")

    # 3. DeepSeek
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    if deepseek_key:
        try:
            print(f"🧠 DeepSeek ishga tushdi ({mode.upper()})...")
            url = "[https://api.deepseek.com/v1/chat/completions](https://api.deepseek.com/v1/chat/completions)"
            headers = {
                "Authorization": f"Bearer {deepseek_key.strip()}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }
            r = requests.post(url, headers=headers, json=payload, timeout=90)
            if r.status_code == 200:
                data = r.json()
                return json.loads(data["choices"][0]["message"]["content"])
            else:
                print(f"⚠️ DeepSeek xatoligi: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"⚠️ DeepSeek ulanish xatoligi: {e}")

    raise RuntimeError("Birorta ham AI provayderi javob bermadi!")
