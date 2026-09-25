import os
import json
import time
import requests
from google import genai


def clean_json_response(raw_text):
    """Parse JSON returned by an AI provider, including fenced responses."""
    if not isinstance(raw_text, str) or not raw_text.strip():
        raise ValueError("AI provider returned an empty response")

    text = raw_text.strip()

    # Remove Markdown code fences if a provider ignores the prompt.
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1:]
        else:
            text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Some models add text around the JSON. Recover the outermost object.
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end <= start:
            raise
        return json.loads(text[start:end + 1])


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


def request_compatible_provider(url, api_key, model, prompt, timeout=90):
    """Call an OpenAI-compatible API and return the provider's JSON object."""
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "response_format": {"type": "json_object"},
        },
        timeout=timeout,
    )

    if not response.ok:
        raise RuntimeError(
            f"HTTP {response.status_code}: {response.text[:500]}"
        )

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return content if isinstance(content, dict) else clean_json_response(content)


def get_unique_story(winning_theme, past_titles, past_hooks, mode="shorts", episode_num=1):
    prompt = build_prompt(mode, winning_theme, past_titles, past_hooks, episode_num)
    provider_errors = []

    # 1. Gemini. The first model is the model recommended by the failed run.
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if gemini_key:
        try:
            client = genai.Client(api_key=gemini_key)
            models_to_try = [
                "gemini-3.8-flash",
                "gemini-2.5-flash",
                "gemini-2.0-flash",
            ]
            for model_name in models_to_try:
                try:
                    print(f"🧠 Gemini ({model_name}) ishga tushdi ({mode.upper()})...")
                    result = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    text = getattr(result, "text", None)
                    if text:
                        return clean_json_response(text)
                    raise ValueError("Gemini returned an empty response")
                except Exception as exc:
                    message = f"Gemini {model_name}: {exc}"
                    provider_errors.append(message)
                    print(f"⚠️ {message}")
                    time.sleep(1)
        except Exception as exc:
            message = f"Gemini initialization: {exc}"
            provider_errors.append(message)
            print(f"⚠️ {message}")
    else:
        print("⚠️ GEMINI_API_KEY mavjud emas, Gemini o'tkazib yuborildi")

    # 2. Groq. Plain URL is intentional; do not use Markdown-link syntax here.
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    if groq_key:
        try:
            print(f"🧠 Groq ishga tushdi ({mode.upper()})...")
            return request_compatible_provider(
                "https://api.groq.com/openai/v1/chat/completions",
                groq_key,
                "llama-3.3-70b-versatile",
                prompt,
                timeout=90,
            )
        except Exception as exc:
            message = f"Groq: {exc}"
            provider_errors.append(message)
            print(f"⚠️ {message}")
    else:
        print("⚠️ GROQ_API_KEY mavjud emas, Groq o'tkazib yuborildi")

    # 3. DeepSeek fallback.
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if deepseek_key:
        try:
            print(f"🧠 DeepSeek ishga tushdi ({mode.upper()})...")
            return request_compatible_provider(
                "https://api.deepseek.com/chat/completions",
                deepseek_key,
                "deepseek-chat",
                prompt,
                timeout=90,
            )
        except Exception as exc:
            message = f"DeepSeek: {exc}"
            provider_errors.append(message)
            print(f"⚠️ {message}")
    else:
        print("⚠️ DEEPSEEK_API_KEY mavjud emas, DeepSeek o'tkazib yuborildi")

    details = " | ".join(provider_errors[-5:])
    raise RuntimeError(
        "Birorta ham AI provayderi javob bermadi. "
        f"Tafsilot: {details}"
    )
