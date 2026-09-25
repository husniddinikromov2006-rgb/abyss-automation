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

    # 1. GEMINI (Google talab qilgan yagona to'g'ri model: gemini-3.8-flash)
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
                    print(f"⚠️ Gemini urinish {attempt} kutilmoqda: {ge}")
                    if attempt < 3:
                        time.sleep(4 * attempt)
        except Exception as e:
            print(f"⚠️ Gemini xatoligi: {e}")

    # 2. GROQ (Toza URL string, markdown belgilarsiz)
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        groq_url = "[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)"
        groq_models = ["llama-3.1-8b-instant", "llama3-70b-8192"]
        for g_model in groq_models:
            try:
                print(f"🧠 Groq ({g_model}) ishga tushdi...")
                headers = {
                    "Authorization": f"Bearer {groq_key.strip()}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": g_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"}
                }
                r = requests.post(groq_url, headers=headers, json=payload, timeout=40)
                if r.status_code == 200:
                    data = r.json()
                    return json.loads(data["choices"][0]["message"]["content"])
                else:
                    print(f"⚠️ Groq ({g_model}) status: {r.status_code}")
            except Exception as e:
                print(f"⚠️ Groq ({g_model}) xatoligi: {e}")

    # 3. ZAXIRA (Pollinations Text API - toza URL)
    print(f"🧠 Zaxira AI ishga tushdi...")
    try:
        poll_url = "[https://text.pollinations.ai/openai/chat/completions](https://text.pollinations.ai/openai/chat/completions)"
        payload = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": "You are a JSON generator. Return only raw valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        pr = requests.post(poll_url, json=payload, timeout=60)
        if pr.status_code == 200:
            return json.loads(pr.json()["choices"][0]["message"]["content"])
    except Exception as pe:
        print(f"⚠️ Zaxira AI xatoligi: {pe}")

    raise RuntimeError("Birorta ham AI javob bermadi!")
