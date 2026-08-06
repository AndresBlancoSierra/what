import { useEffect, useRef, useState } from "react";
import { Play, Pause } from "lucide-react";

interface Props {
  audioUrl: string;
  onTimeUpdate: (time: number) => void;
  onLoaded: (duration: number) => void;
  audioRef: React.RefObject<HTMLAudioElement | null>;
  playing: boolean;
  setPlaying: (v: boolean) => void;
}

export default function AudioPlayer({ audioUrl, onTimeUpdate, onLoaded, audioRef, playing, setPlaying }: Props) {
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    if (!audioRef.current) return;
    const audio = audioRef.current;

    const handleTime = () => onTimeUpdate(audio.currentTime);
    const handleLoaded = () => {
      setDuration(audio.duration);
      onLoaded(audio.duration);
    };
    const handleEnd = () => setPlaying(false);

    audio.addEventListener("timeupdate", handleTime);
    audio.addEventListener("loadedmetadata", handleLoaded);
    audio.addEventListener("ended", handleEnd);

    return () => {
      audio.removeEventListener("timeupdate", handleTime);
      audio.removeEventListener("loadedmetadata", handleLoaded);
      audio.removeEventListener("ended", handleEnd);
    };
  }, [audioUrl]);

  useEffect(() => {
    if (!audioRef.current) return;
    if (playing) {
      audioRef.current.play().catch(() => setPlaying(false));
    } else {
      audioRef.current.pause();
    }
  }, [playing]);

  function togglePlay() {
    setPlaying(!playing);
  }

  function formatTime(t: number) {
    const m = Math.floor(t / 60);
    const s = Math.floor(t % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }

  return (
    <div className="flex items-center gap-4 rounded-xl border border-border bg-bg-card px-5 py-4">
      <button
        onClick={togglePlay}
        className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-accent text-bg transition-opacity hover:opacity-80"
      >
        {playing ? <Pause size={20} /> : <Play size={20} />}
      </button>
      <div className="flex-1">
        <div className="h-2 rounded-full bg-border">
          <div
            className="h-full rounded-full bg-accent transition-all"
            style={{
              width: duration
                ? `${((audioRef.current?.currentTime ?? 0) / duration) * 100}%`
                : "0%",
            }}
          />
        </div>
      </div>
      <span className="shrink-0 text-xs text-text-muted tabular-nums">
        {formatTime(audioRef.current?.currentTime ?? 0)} / {formatTime(duration)}
      </span>
      <audio ref={audioRef} src={audioUrl} preload="auto" />
    </div>
  );
}
