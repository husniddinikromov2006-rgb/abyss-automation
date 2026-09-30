"""Automatically choose background music that matches generated travel footage.

The selector uses yt-dlp search instead of a hard-coded YouTube URL.  It only
returns a file after ffprobe confirms that the download contains an audio
stream.  Use a royalty-free/Creative Commons source or your own licensed
music when publishing the generated videos.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Iterable, Mapping


MUSIC_DIR = Path(os.getenv("MUSIC_DIR", "music"))
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

# Search phrases are deliberately descriptive: yt-dlp will pick a suitable
# result from the requested mood/style instead of always reusing one song.
_STYLE_BY_KEYWORD = {
    "AI WORLD": "cinematic ambient fantasy instrumental",
    "ALIEN WORLD": "cinematic sci-fi ambient instrumental",
    "COSMIC WORLD": "space ambient cinematic instrumental",
    "desert": "ethnic cinematic desert instrumental",
    "beach": "tropical chill travel instrumental",
    "island": "tropical cinematic travel instrumental",
    "ocean": "cinematic ocean ambient instrumental",
    "waterfall": "peaceful nature ambient instrumental",
    "forest": "calm forest nature documentary instrumental",
    "lake": "peaceful cinematic travel piano instrumental",
    "mountain": "epic cinematic mountain travel instrumental",
    "glacier": "cinematic arctic ambient instrumental",
}


def _has_audio_stream(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size == 0:
        return False
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=codec_type",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ], capture_output=True, text=True, check=False,
    )
    return result.returncode == 0 and result.stdout.strip() == "audio"


def _music_query(spots: Iterable[Mapping[str, str]]) -> str:
    text = " ".join(
        f"{spot.get('country', '')} {spot.get('query', '')}"
        for spot in spots
    ).lower()
    for keyword, style in _STYLE_BY_KEYWORD.items():
        if keyword.lower() in text:
            return style
    return "cinematic nature travel documentary instrumental"


def get_matching_audio_file(
    spots: Iterable[Mapping[str, str]], short_index: int,
) -> str:
    """Download and return music selected from the video's locations.

    ``yt-dlp`` searches YouTube for an instrumental result.  The caller should
    pass the same spots used to build the short, so the music mood follows the
    footage.  ``MUSIC_URL`` can be set to a licensed direct URL to bypass
    search entirely.
    """
    direct_url = os.getenv("MUSIC_URL")
    query = _music_query(spots)
    target = MUSIC_DIR / f"auto_music_{short_index}.%(ext)s"
    expected = MUSIC_DIR / f"auto_music_{short_index}.mp3"

    if _has_audio_stream(expected):
        return str(expected.resolve())

    source = direct_url or f"ytsearch1:{query} royalty free no copyright"
    print(f"[AUDIO]: Video uchun mos musiqa qidirilmoqda: {query}")
    subprocess.run(
        [
            "yt-dlp", "--no-playlist", "--extract-audio",
            "--audio-format", "mp3", "--audio-quality", "0",
            "--force-overwrites", "--no-warnings",
            "--output", str(target), source,
        ], check=True,
    )

    if not _has_audio_stream(expected):
        raise RuntimeError(f"Mos musiqa yuklanmadi yoki audio stream yo'q: {expected}")
    print(f"[AUDIO TAYYOR]: {expected}")
    return str(expected.resolve())


__all__ = ["get_matching_audio_file"]
