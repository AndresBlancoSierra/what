import { useState } from "react";
import { Trash2 } from "lucide-react";
import { deleteSong } from "../api/client";
import type { SongSummary } from "../api/client";

interface Props {
  song: SongSummary;
  onDeleted: () => void;
}

export default function SongCard({ song, onDeleted }: Props) {
  const [deleting, setDeleting] = useState(false);
  const [showDelete, setShowDelete] = useState(false);

  async function handleDelete(e: React.MouseEvent) {
    e.stopPropagation();
    if (deleting) return;
    setDeleting(true);
    try {
      await deleteSong(song.id);
      onDeleted();
    } catch {
      setDeleting(false);
    }
  }

  return (
    <div
      style={{
        position: "relative",
        padding: 16,
        borderRadius: 12,
        border: "1px solid var(--color-border)",
        backgroundColor: "var(--color-bg-card)",
        transition: "all 0.15s",
      }}
      onMouseEnter={() => setShowDelete(true)}
      onMouseLeave={() => setShowDelete(false)}
    >
      <button
        onClick={handleDelete}
        disabled={deleting}
        style={{
          position: "absolute",
          right: 12,
          top: 12,
          width: 32,
          height: 32,
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          border: "none",
          cursor: "pointer",
          backgroundColor: "transparent",
          color: showDelete ? "var(--color-danger)" : "transparent",
          transition: "color 0.15s",
        }}
      >
        <Trash2 size={14} />
      </button>
      <h3 style={{ fontWeight: 600, color: "var(--color-text)", paddingRight: 32 }}>{song.title}</h3>
      <p style={{ marginTop: 4, fontSize: 14, color: "var(--color-text-secondary)" }}>{song.artist}</p>
      <div style={{ marginTop: 12, display: "flex", alignItems: "center", gap: 12, fontSize: 12, color: "var(--color-text-muted)" }}>
        <span>{song.duration ? `${Math.round(song.duration / 60)}m` : "?"}</span>
        <span>{song.segments_count} segments</span>
      </div>
    </div>
  );
}
