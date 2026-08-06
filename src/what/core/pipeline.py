from loguru import logger
from what.core.search import search_youtube
from what.core.downloader import download_audio, get_audio_duration
from what.core.lyrics import get_lyrics
from what.core.transcriber import transcribe
from what.core.aligner import align


class Pipeline:
    def __init__(self):
        self.steps = []

    def run(self, youtube_url: str, title: str, artist: str) -> dict:
        logger.info(f"Pipeline started for {artist} - {title}")

        logger.info(f"Downloading audio from {youtube_url}")
        audio_path = download_audio(youtube_url)
        logger.info(f"Audio saved to {audio_path}")

        duration = get_audio_duration(audio_path)
        logger.info(f"Audio duration: {duration}s")

        logger.info(f"Fetching lyrics for {artist} - {title}")
        lyrics_text = get_lyrics(title, artist)
        logger.info(f"Lyrics fetched ({len(lyrics_text)} chars)")

        logger.info("Transcribing audio with faster-whisper large-v3")
        whisper_segments = transcribe(audio_path)
        logger.info(f"Transcription complete: {len(whisper_segments)} segments")

        logger.info("Aligning lyrics with timestamps")
        aligned = align(lyrics_text, whisper_segments)
        logger.info(f"Aligned {len(aligned)} segments")

        return {
            "title": title,
            "artist": artist,
            "youtube_url": youtube_url,
            "audio_path": audio_path,
            "duration": duration,
            "lyrics_text": lyrics_text,
            "segments": aligned,
        }
