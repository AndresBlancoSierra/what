import { useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Loader2 } from "lucide-react";
import { getSong, getAudioUrl, exportSong, type Segment } from "../api/client";
import AudioPlayer from "../components/AudioPlayer";
import LyricsViewer from "../components/LyricsViewer";
import ExportButton from "../components/ExportButton";

export default function SongPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [currentSegment, setCurrentSegment] = useState<Segment | null>(null);

  const { data: song, isLoading, error } = useQuery({
    queryKey: ["song", id],
    queryFn: () => getSong(id!),
    enabled: !!id,
  });

  function handleLineClick(seg: Segment) {
    if (!audioRef.current) return;
    audioRef.current.currentTime = seg.start_time;
    setCurrentSegment(seg);
    setPlaying(true);
  }

  function handleTimeUpdate(time: number) {
    setCurrentTime(time);
    if (currentSegment && time >= currentSegment.end_time) {
      if (audioRef.current) {
        audioRef.current.pause();
        setPlaying(false);
        setCurrentSegment(null);
      }
    }
  }

  function handleLoaded(_duration: number) {}

  async function handleExport() {
    if (!id) return;
    await exportSong(id);
  }

  if (isLoading) {
    return (
      <div className="flex min-h-dvh items-center justify-center">
        <div className="flex items-center gap-2 text-text-muted">
          <Loader2 size={16} className="animate-spin" />
          Loading song...
        </div>
      </div>
    );
  }

  if (error || !song) {
    return (
      <div className="flex min-h-dvh items-center justify-center px-6">
        <div className="w-full max-w-lg rounded-xl border border-border bg-bg-card px-5 py-3 text-sm text-danger">
          {String(error || "Song not found")}
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto flex min-h-dvh w-full max-w-lg flex-col px-6 py-8">
      <button
        onClick={() => navigate("/")}
        className="mb-6 flex items-center gap-1.5 text-sm text-text-secondary transition hover:text-text"
      >
        <ArrowLeft size={16} />
        Back to library
      </button>

      <div className="mb-6 flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold text-text" style={{ fontWeight: 900 }}>
            {song.title}
          </h1>
          <p className="mt-1 text-text-secondary">{song.artist}</p>
        </div>
        <ExportButton songId={song.id} onExport={handleExport} />
      </div>

      <AudioPlayer
        audioUrl={getAudioUrl(song.id)}
        onTimeUpdate={handleTimeUpdate}
        onLoaded={handleLoaded}
        audioRef={audioRef}
        playing={playing}
        setPlaying={setPlaying}
      />

      <div className="mt-8 flex-1 rounded-xl border border-border bg-bg-card p-5">
        <h2 className="mb-4 text-xs font-semibold tracking-widest text-text-muted">
          LYRICS
        </h2>
        <LyricsViewer
          segments={song.segments}
          currentTime={currentTime}
          onLineClick={handleLineClick}
          audioRef={audioRef}
        />
      </div>
    </div>
  );
}
