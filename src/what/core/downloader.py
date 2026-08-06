import logging
import subprocess
from pathlib import Path
from what.config.settings import settings

logger = logging.getLogger(__name__)


def download_audio(url: str, output_dir: Path | None = None) -> str:
    if output_dir is None:
        output_dir = settings.data_dir

    output_dir.mkdir(parents=True, exist_ok=True)
    template = str(output_dir / "%(id)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "wav",
        "--audio-quality", "0",
        "-o", template,
        "--no-update",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    log = (result.stdout + result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp download failed: {result.stderr.strip()[:500]}")

    output_paths = list(output_dir.glob("*.wav"))
    if not output_paths:
        raise RuntimeError(f"No WAV files found in {output_dir} after download")

    latest = max(output_paths, key=lambda p: p.stat().st_mtime)
    resolved = str(latest.resolve())
    logger.info(f"Audio downloaded to {resolved}")
    return resolved


def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        audio_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    raw = result.stdout.strip()
    if not raw:
        logger.warning(f"ffprobe returned empty duration for {audio_path}")
        return 0.0
    try:
        return float(raw)
    except ValueError:
        logger.warning(f"ffprobe non-numeric duration '{raw}' for {audio_path}")
        return 0.0
