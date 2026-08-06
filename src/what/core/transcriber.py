import logging
from faster_whisper import WhisperModel
from what.config.settings import settings

logger = logging.getLogger(__name__)

_model = None


def _get_model():
    global _model
    if _model is None:
        model_size = settings.whisper.get("model_size", "large-v3")
        device = settings.whisper.get("device", "auto")
        compute_type = settings.whisper.get("compute_type", "float16")

        if device == "cpu":
            compute_type = "int8"

        if device == "auto":
            try:
                import ctranslate2
                if ctranslate2.get_cuda_device_count() > 0:
                    logger.info("CUDA detected, using GPU")
                    device = "cuda"
                else:
                    device = "cpu"
                    compute_type = "int8"
            except Exception:
                logger.info("CUDA not available, falling back to CPU")
                device = "cpu"
                compute_type = "int8"

        logger.info(f"Loading faster-whisper {model_size} on {device} ({compute_type})")
        try:
            _model = WhisperModel(model_size, device=device, compute_type=compute_type)
        except Exception as e:
            if device == "cuda":
                logger.warning(f"CUDA init failed ({e}), falling back to CPU")
                _model = WhisperModel(model_size, device="cpu", compute_type="int8")
            else:
                raise
    return _model


def transcribe(audio_path: str) -> list[dict]:
    model = _get_model()
    segments, info = model.transcribe(
        audio_path,
        word_timestamps=True,
        beam_size=5,
    )

    result = []
    for seg in segments:
        words = [
            {"text": w.word, "start": w.start, "end": w.end}
            for w in (seg.words or [])
        ]
        result.append({
            "text": seg.text.strip(),
            "start": seg.start,
            "end": seg.end,
            "words": words,
        })

    return result
