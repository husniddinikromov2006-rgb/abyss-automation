import os
import json
import requests
from google import genai

def build_anti_repetition_prompt(winning_theme, past_titles, past_hooks):
    past_titles_str = "\n- ".join(past_titles[-15:]) if past_titles else "None yet"
    past_hooks_str = "\n- ".join(past_hooks[-15:]) if past_hooks else "None yet"

    return (
        "You are an elite Hollywood mystery-thriller director. Write an intense, terrifying fictional US naval abyss/deep-sea horror story (50 seconds spoken pace).\n"
        f"ANALYTICS INSIGHT: High engagement theme from channel data is: '{winning_theme}'. Lean into this atmosphere.\n"
        "STRICT ZERO-REPETITION RULES:\n"
        "1. DO NOT use generic openings like 'More people have walked on the moon', 'Deep beneath the ocean', or 'In the dark abyss'.\n"
        "2. FORBIDDEN RECENT TITLES (DO NOT COPY OR REPHRASE):\n"
        f"- {past_titles_str}\n"
        "3. FORBIDDEN OPENING HOOKS (DO NOT USE THESE PHRASES OR SIMILAR STRUCTURES):\n"
        f"- {past_hooks_str}\n"
        "4. Use diverse naval assets: bathyscaphes, acoustic research towers, cold war sea stations, deep seismic drills, nuclear submarine reactors.\n"
        "5. The story MUST be split into exactly 12 scenes (3-4 seconds per scene).\n"
        "Return ONLY a raw JSON object with this exact schema (no markdown, no backticks):\n"
        "{\n"
        '  "title": "short click-worthy title (under 55 chars) with 1 emoji and #Shorts",\n'
        '  "hook": "the exact first 10 spoken words that grab instant attention",\n'
        '  "script": "Full narrative script (roughly 110-130 words)",\n'
        '  "scenes": [\n'
        '     {"text": "spoken narration line", "prompt": "8k photorealistic dark underwater cinematic horror prompt, Unreal Engine 5, hyper-detailed"}\n'
        "  ]\n"
        "}"
    )

def clean_json_response(raw_text):
    text = raw_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

def generate_story_with_gemini(api_key, prompt):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return clean_json_response(response.text)

def generate_story_with_deepseek(api_key, prompt):
    url = "[https://api.deepseek.com/v1/chat/completions](https://api.deepseek.com/v1/chat/completions)"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    if r.status_code == 200:
        return json.loads(r.json()["choices"][0]["message"]["content"])
    raise Exception(f"DeepSeek status: {r.status_code}")

def generate_story_with_groq(api_key, prompt):
    url = "[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    r = requests.post(url, headers=headers, json=payload, timeout=40)
    if r.status_code == 200:
        return json.loads(r.json()["choices"][0]["message"]["content"])
    raise Exception(f"Groq status: {r.status_code}")

def get_unique_story(winning_theme, past_titles, past_hooks):
    prompt = build_anti_repetition_prompt(winning_theme, past_titles, past_hooks)

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            print("🧠 Gemini 2.5 tahlil va takrorlanmas ssenariy yaratmoqda...")
            return generate_story_with_gemini(gemini_key, prompt)
        except Exception as e:
            print(f"⚠️ Gemini xatoligi: {e}")

    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    if deepseek_key:
        try:
            print("🧠 DeepSeek takrorlanmas ssenariy yaratmoqda...")
            return generate_story_with_deepseek(deepseek_key, prompt)
        except Exception as e:
            print(f"⚠️ DeepSeek xatoligi: {e}")

    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            print("🧠 Groq Llama-3.3 ishga tushdi...")
            return generate_story_with_groq(groq_key, prompt)
        except Exception as e:
            print(f"⚠️ Groq xatoligi: {e}")

    raise RuntimeError("Birorta ham AI provayderi javob bermadi!")
