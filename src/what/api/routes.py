import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from what.database.engine import get_session
from what.database import repository as repo
from what.core.pipeline import Pipeline
from what.core.search import search_youtube
from what.core.exporter import export_song
from what.core.lyrics import get_lyrics
from what.config.settings import settings

router = APIRouter()
_pipeline = Pipeline()


class ProcessRequest(BaseModel):
    youtube_url: str
    title: str
    artist: str


class SearchResult(BaseModel):
    title: str
    artist: str
    url: str
    duration: int
    full_title: str


class SongResponse(BaseModel):
    id: str
    title: str
    artist: str
    youtube_url: str
    duration: float
    created_at: str


class SegmentResponse(BaseModel):
    id: int
    line_number: int
    text: str
    start_time: float
    end_time: float


class SongDetailResponse(SongResponse):
    lyrics_text: str
    segments: list[SegmentResponse]


@router.get("/search")
async def search(q: str):
    try:
        results = search_youtube(q, max_results=8)
        return {"results": results}
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/songs")
async def process_song(req: ProcessRequest):
    try:
        result = _pipeline.run(
            youtube_url=req.youtube_url,
            title=req.title,
            artist=req.artist,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    async with await get_session() as session:
        song = await repo.create_song(
            session=session,
            title=result["title"],
            artist=result["artist"],
            audio_path=result["audio_path"],
            lyrics_text=result["lyrics_text"],
            duration=result["duration"],
            youtube_url=result["youtube_url"],
        )
        await repo.add_segments(session, song.id, result["segments"])

        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "duration": song.duration,
            "segments_count": len(result["segments"]),
            "created_at": song.created_at,
        }


@router.get("/songs")
async def list_songs():
    async with await get_session() as session:
        songs = await repo.get_all_songs(session)
        return {
            "songs": [
                {
                    "id": s.id,
                    "title": s.title,
                    "artist": s.artist,
                    "duration": s.duration,
                    "segments_count": len(s.segments),
                    "created_at": s.created_at,
                }
                for s in songs
            ]
        }


@router.get("/songs/{song_id}")
async def get_song(song_id: str):
    async with await get_session() as session:
        song = await repo.get_song_with_segments(session, song_id)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "youtube_url": song.youtube_url,
            "audio_path": song.audio_path,
            "duration": song.duration,
            "lyrics_text": song.lyrics_text,
            "created_at": song.created_at,
            "segments": [
                {
                    "id": seg.id,
                    "line_number": seg.line_number,
                    "text": seg.text,
                    "start_time": seg.start_time,
                    "end_time": seg.end_time,
                }
                for seg in song.segments
            ],
        }


@router.get("/songs/{song_id}/audio")
async def stream_audio(song_id: str):
    async with await get_session() as session:
        song = await repo.get_song(session, song_id)
        if not song or not song.audio_path:
            raise HTTPException(status_code=404, detail="Audio not found")
        audio_path = Path(song.audio_path)
        if not audio_path.exists():
            raise HTTPException(status_code=404, detail="Audio file not found on disk")
        return FileResponse(
            str(audio_path),
            media_type="audio/wav",
            filename=f"{song.artist} - {song.title}.wav",
        )


@router.delete("/songs/{song_id}")
async def delete_song(song_id: str):
    async with await get_session() as session:
        deleted = await repo.delete_song(session, song_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Song not found")
        return {"deleted": True}


@router.post("/songs/{song_id}/export")
async def export_song_endpoint(song_id: str):
    async with await get_session() as session:
        song = await repo.get_song_with_segments(session, song_id)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        if not song.audio_path:
            raise HTTPException(status_code=400, detail="No audio file for this song")

        audio_path = Path(song.audio_path)
        if not audio_path.exists():
            raise HTTPException(status_code=404, detail="Audio file not found on disk")

        segments = [
            {
                "line_number": seg.line_number,
                "text": seg.text,
                "start_time": seg.start_time,
                "end_time": seg.end_time,
            }
            for seg in song.segments
        ]

        try:
            export_dir = export_song(
                title=song.title,
                artist=song.artist,
                audio_path=str(audio_path),
                segments=segments,
            )
            return {
                "export_path": str(export_dir),
                "segments_count": len(segments),
                "message": f"Exported to {export_dir}",
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
