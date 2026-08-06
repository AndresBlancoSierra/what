import os
import re
import httpx
from what.config.settings import settings

GENIUS_API = "https://api.genius.com"


def _get_access_token() -> str:
    token = os.environ.get("GENIUS_ACCESS_TOKEN", "") or settings.genius.get("access_token", "")
    if not token:
        raise ValueError(
            "Genius access token not configured. "
            "Set GENIUS_ACCESS_TOKEN in the environment or "
            "genius.access_token in configs/default.yaml"
        )
    return token


def search_song(title: str, artist: str) -> dict | None:
    token = _get_access_token()
    query = f"{artist} {title}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = httpx.get(
        f"{GENIUS_API}/search",
        params={"q": query},
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    translation_kw = ["translation", "traduzione", "traducción", "traduction", " übersetzung", "italian", "spanish", "french", "german", "portuguese"]

    hits = data.get("response", {}).get("hits", [])
    for hit in hits:
        result = hit.get("result", {})
        result_artist = result.get("primary_artist", {}).get("name", "").lower()
        result_title = result.get("title", "").lower()
        if artist.lower() in result_artist or artist.lower() in result_title:
            if any(kw in result_title for kw in translation_kw):
                continue
            return {
                "id": result["id"],
                "title": result["title"],
                "artist": result["primary_artist"]["name"],
                "url": result["url"],
            }

    for hit in hits:
        result = hit.get("result", {})
        result_title = result.get("title", "").lower()
        if any(kw in result_title for kw in translation_kw):
            continue
        return {
            "id": result["id"],
            "title": result["title"],
            "artist": result["primary_artist"]["name"],
            "url": result["url"],
        }

    return None


def fetch_lyrics(genius_url: str) -> str:
    resp = httpx.get(genius_url, timeout=15, follow_redirects=True)
    resp.raise_for_status()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")

    containers = soup.select("[data-lyrics-container]")
    parts = []
    for div in containers:
        classes = div.get("class", [])
        class_str = " ".join(classes) if isinstance(classes, list) else str(classes)
        text = div.get_text(strip=True)
        if not text:
            continue

        html = div.decode_contents()
        html = html.replace("<br/>", "\n").replace("<br>", "\n")
        for tag in ["i", "em", "b", "a", "span"]:
            html = html.replace(f"<{tag}>", "").replace(f"</{tag}>", "")
        html = re.sub(r"<[^>]+>", "", html)
        text = html.strip()
        if text and not any(
            kw in text.lower() for kw in ["translations", "contributors", "share this"]
        ):
            parts.append(text)

    return "\n".join(parts)


def get_lyrics(title: str, artist: str) -> str:
    if not title.strip():
        raise ValueError("Song title is empty")

    sanitized = re.sub(r"\s*\((Explicit|Clean|Lyrics|Official Video|Music Video|Audio)\)\s*", "", title, flags=re.IGNORECASE).strip()
    song = search_song(sanitized, artist)
    if not song:
        raise ValueError(f"Could not find '{title}' by '{artist or 'unknown'}' on Genius")

    lyrics = fetch_lyrics(song["url"])
    if not lyrics:
        raise ValueError(f"Could not fetch lyrics from {song['url']}")

    return lyrics
