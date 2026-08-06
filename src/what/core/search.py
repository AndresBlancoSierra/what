import json
import logging
import re
import subprocess

logger = logging.getLogger(__name__)


def parse_title(title: str) -> tuple[str, str]:
    parts = re.split(r"\s*[-–—|]\s*", title, maxsplit=1)
    if len(parts) == 2:
        artist = parts[0].strip()
        song_title = re.sub(
            r"\s*\(.*?Official.*?\)\s*$|\s*\[.*?\]\s*$|\s*Lyrics.*$",
            "",
            parts[1].strip(),
        ).strip()
        return artist, song_title
    return "", title.strip()


def search_youtube(query: str, max_results: int = 10) -> list[dict]:
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{query}",
        "--flat-playlist",
        "--dump-json",
        "--no-download",
        "--no-update",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        raise RuntimeError("yt-dlp search timed out")
    except FileNotFoundError:
        raise RuntimeError("yt-dlp not found on system")

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "Connection refused" in stderr or "Unable to download" in stderr:
            logger.warning(f"YouTube search unavailable: {stderr[:200]}")
            return []
        raise RuntimeError(f"yt-dlp search failed: {stderr[:500]}")

    results = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        title = data.get("title", "")
        artist, song_title = parse_title(title)
        results.append({
            "title": song_title or title,
            "artist": artist or data.get("channel", ""),
            "url": data.get("webpage_url", ""),
            "duration": data.get("duration", 0),
            "full_title": title,
        })
    return results
