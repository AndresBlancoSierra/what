import re
import difflib


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s']", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _words(text: str) -> set[str]:
    return set(_normalize(text).split())


def align(lyrics_text: str, whisper_segments: list[dict]) -> list[dict]:
    lyrics_lines = [
        l.strip() for l in lyrics_text.split("\n")
        if l.strip() and not l.strip().startswith("[")
    ]
    lyrics_lines = [
        re.sub(r"\[.*?\]", "", l).strip()
        for l in lyrics_lines
    ]
    lyrics_lines = [l for l in lyrics_lines if l]

    if not lyrics_lines:
        return []

    norm_lines = [_normalize(l) for l in lyrics_lines]
    norm_segs = [_normalize(s["text"]) for s in whisper_segments]

    result = []
    used_segments = set()

    for i, (orig_line, norm_line) in enumerate(zip(lyrics_lines, norm_lines)):
        if not norm_line:
            continue

        best_idx = -1
        best_score = 0.0
        line_words = _words(orig_line)

        for j, ns in enumerate(norm_segs):
            if j in used_segments:
                continue
            ratio = difflib.SequenceMatcher(None, norm_line, ns).ratio()
            seg_words = _words(whisper_segments[j]["text"])
            word_overlap = 0
            if line_words:
                overlap = len(line_words & seg_words)
                word_overlap = overlap / max(len(line_words), 1)

            score = max(ratio, word_overlap * 0.8)
            if score > best_score:
                best_score = score
                best_idx = j

        if best_idx >= 0 and best_score > 0.15:
            used_segments.add(best_idx)
            result.append({
                "line_number": i + 1,
                "text": orig_line,
                "start_time": whisper_segments[best_idx]["start"],
                "end_time": whisper_segments[best_idx]["end"],
            })
        else:
            result.append({
                "line_number": i + 1,
                "text": orig_line,
                "start_time": 0.0,
                "end_time": 0.0,
            })

    return result
