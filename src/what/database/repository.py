import uuid
from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from what.database.models import Song, Segment


async def create_song(
    session: AsyncSession,
    title: str,
    artist: str,
    audio_path: str,
    lyrics_text: str,
    duration: float = 0.0,
    youtube_url: str = "",
) -> Song:
    song_id = uuid.uuid4().hex[:12]
    song = Song(
        id=song_id,
        title=title,
        artist=artist,
        youtube_url=youtube_url,
        audio_path=audio_path,
        duration=duration,
        lyrics_text=lyrics_text,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song


async def add_segments(
    session: AsyncSession,
    song_id: str,
    segments: list[dict],
) -> list[Segment]:
    objs = [
        Segment(
            song_id=song_id,
            line_number=s["line_number"],
            text=s["text"],
            start_time=s["start_time"],
            end_time=s["end_time"],
        )
        for s in segments
    ]
    session.add_all(objs)
    await session.commit()
    for obj in objs:
        await session.refresh(obj)
    return objs


async def get_all_songs(session: AsyncSession) -> list[Song]:
    from sqlalchemy.orm import selectinload
    result = await session.execute(
        select(Song).order_by(Song.created_at.desc())
        .options(selectinload(Song.segments))
    )
    return list(result.scalars().all())


async def get_song(session: AsyncSession, song_id: str) -> Song | None:
    result = await session.execute(select(Song).where(Song.id == song_id))
    return result.scalar_one_or_none()


async def get_song_with_segments(session: AsyncSession, song_id: str) -> Song | None:
    from sqlalchemy.orm import selectinload
    result = await session.execute(
        select(Song).where(Song.id == song_id)
        .options(selectinload(Song.segments))
    )
    return result.scalar_one_or_none()


async def delete_song(session: AsyncSession, song_id: str) -> bool:
    song = await get_song(session, song_id)
    if not song:
        return False
    await session.delete(song)
    await session.commit()
    return True
