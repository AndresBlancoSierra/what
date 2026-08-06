import os
import re
import subprocess
from pathlib import Path
from what.config.settings import settings


def _sanitize(name: str) -> str:
    return re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")


def export_song(title: str, artist: str, audio_path: str, segments: list[dict]) -> Path:
    safe_name = f"{_sanitize(artist)}_{_sanitize(title)}"
    export_dir = settings.anki_dir / safe_name
    export_dir.mkdir(parents=True, exist_ok=True)

    for seg in segments:
        line_num = seg["line_number"]
        start = seg["start_time"]
        end = seg["end_time"]

        if end <= start:
            continue

        mp3_path = export_dir / f"{line_num:03d}.mp3"
        txt_path = export_dir / f"{line_num:03d}.txt"

        cmd = [
            "ffmpeg",
            "-y",
            "-i", audio_path,
            "-ss", str(start),
            "-to", str(end),
            "-c:a", "libmp3lame",
            "-b:a", "64k",
            "-vn",
            str(mp3_path),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        txt_path.write_text(seg["text"] + "\n", encoding="utf-8")

    return export_dir
