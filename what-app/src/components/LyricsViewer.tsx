import { useRef, useEffect } from "react";
import type { Segment } from "../api/client";

interface Props {
  segments: Segment[];
  currentTime: number;
  onLineClick: (segment: Segment) => void;
  audioRef: React.RefObject<HTMLAudioElement | null>;
}

export default function LyricsViewer({ segments, currentTime, onLineClick, audioRef }: Props) {
  const activeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (activeRef.current) {
      activeRef.current.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, [currentTime]);

  function isActive(seg: Segment) {
    return currentTime >= seg.start_time && currentTime < seg.end_time;
  }

  return (
    <div className="space-y-1">
      {segments.map((seg) => {
        const active = isActive(seg);
        return (
          <button
            key={seg.id}
            ref={active ? activeRef : undefined}
            onClick={() => {
              if (audioRef.current) {
                onLineClick(seg);
              }
            }}
            className={`w-full rounded-lg px-4 py-3 text-left transition ${
              active
                ? "bg-accent/15 font-medium text-accent"
                : "text-text-secondary hover:bg-bg-hover hover:text-text"
            }`}
          >
            <span className="mr-4 inline-block w-8 text-right text-xs text-text-muted">
              {String(seg.line_number).padStart(2, "0")}
            </span>
            {seg.text}
          </button>
        );
      })}
    </div>
  );
}
