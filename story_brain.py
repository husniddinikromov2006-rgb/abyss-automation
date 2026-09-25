import os
import json
import time
import re
import requests
from google import genai

def clean_url(url_str):
    match = re.search(r'https?://[^\s\)\]\"\']+', url_str)
    if match:
        return match.group(0)
    return url_str.strip()

def clean_json_response(raw_text):
    text = raw_text.strip()
    # Markdown qavslar va belgilarni tozalash
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    # Agar matn ichida JSON obyekt bo'lsa, qidirib olish
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1:
        text = text[start_idx:end_idx + 1]
        
    return json.loads(text)

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
            "}"
        )

    elif mode == "long_3min":
        return (
            "You are an elite documentary director. Write an intense 3-minute standalone horizontal military naval mystery (~400 words).\n"
            f"Context: '{winning_theme}'.\n"
            "RULES:\n"
            "1. NO CLICHE OPENINGS.\n"
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
            "}"
        )

    elif mode == "post":
        return (
            "Create an intriguing Community Post update for a deep ocean mystery YouTube channel.\n"
            "Return ONLY raw valid JSON:\n"
            "{\n"
            '  "title": "Community Post Update",\n'
            '  "text": "Intriguing declassified expedition report update ending with a question (~60-80 words).",\n'
            '  "image_prompt": "16:9 cinematic classified black and white polaroid photograph of underwater expedition in dark ocean, 8k"\n'
            "}"
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
            "}"
        )

def get_unique_story(winning_theme, past_titles, past_hooks, mode="shorts", episode_num=1):
    prompt = build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num)

    # 1. GEMINI
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            client = genai.Client(api_key=gemini_key.strip())
            for attempt in range(1, 4):
                try:
                    print(f"🧠 Gemini (gemini-3.8-flash) urinish {attempt}/3...")
                    res = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
                    if res and res.text:
                        return clean_json_response(res.text)
                except Exception as ge:
                    print(f"⚠️ Gemini urinish {attempt}: {ge}")
                    if attempt < 3:
                        time.sleep(4)
        except Exception as e:
            print(f"⚠️ Gemini ishga tushmadi: {e}")

    # 2. POLLINATIONS AI (Har doim 200 beruvchi mustahkam zaxira)
    print(f"🧠 Zaxira AI ishga tushdi ({mode.upper()})...")
    poll_urls = [
        "[https://text.pollinations.ai/](https://text.pollinations.ai/)",
        "[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)"
    ]

    # Usul A: To'g'ridan-to'g'ri prompt jo'natish
    try:
        url = clean_url(f"[https://text.pollinations.ai/](https://text.pollinations.ai/){requests.utils.quote(prompt)}?json=true")
        r = requests.get(url, timeout=60)
        if r.status_code == 200 and r.text:
            return clean_json_response(r.text)
    except Exception as e:
        print(f"⚠️ Pollinations A usuli kutilmoqda: {e}")

    # Usul B: OpenAI endpoint usuli
    try:
        url = clean_url("[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)")
        payload = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": "You are a professional documentary script JSON generator. Output only valid raw JSON."},
                {"role": "user", "content": prompt}
            ],
            "jsonMode": True
        }
        r = requests.post(url, json=payload, timeout=60)
        if r.status_code == 200:
            try:
                res_data = r.json()
                if "choices" in res_data and len(res_data["choices"]) > 0:
                    content = res_data["choices"][0].get("message", {}).get("content", "")
                    return clean_json_response(content)
                elif "content" in res_data:
                    return clean_json_response(res_data["content"])
            except Exception:
                return clean_json_response(r.text)
    except Exception as e:
        print(f"⚠️ Pollinations B usuli xatoligi: {e}")

    raise RuntimeError("AI tizimlaridan ssenariyni olib bo'lmadi!")
