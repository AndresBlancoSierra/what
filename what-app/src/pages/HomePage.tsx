import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import SearchBar from "../components/SearchBar";
import SongCard from "../components/SongCard";
import { listSongs, processSong } from "../api/client";
import type { SearchResult } from "../api/client";

export default function HomePage() {
  const navigate = useNavigate();
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");

  const { data: songs, isLoading, refetch } = useQuery({
    queryKey: ["songs"],
    queryFn: listSongs,
  });

  const hasSongs = songs && songs.length > 0;

  async function handleSelect(result: SearchResult) {
    setProcessing(true);
    setError("");
    try {
      const summary = await processSong(result.url, result.title, result.artist);
      navigate(`/song/${summary.id}`);
    } catch (e) {
      setError(String(e));
      setProcessing(false);
    }
  }

  return (
    <div className="min-h-dvh overflow-y-auto" style={{ backgroundColor: "var(--color-bg)" }}>
      <section
        className="flex flex-col items-center justify-center"
        style={{ padding: "48px 24px", minHeight: hasSongs ? "50vh" : "85vh" }}
      >
        <div className="flex w-full max-w-lg flex-col items-center" style={{ gap: 40 }}>
          <div className="text-center">
            <h1 className="flex items-baseline justify-center leading-none" style={{ fontSize: "clamp(3rem, 8vw, 5.5rem)", fontWeight: 900 }}>
              <motion.span
                initial={{ letterSpacing: "0.12em", opacity: 0 }}
                animate={{ letterSpacing: "-0.02em", opacity: 1 }}
                transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
              >
                WH
              </motion.span>
              <motion.span
                initial={{ letterSpacing: "0.12em", opacity: 0 }}
                animate={{ letterSpacing: "-0.02em", opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
              >
                AT
              </motion.span>
              <motion.span
                className="inline-block"
                initial={{ y: 0 }}
                animate={{ y: [0, -6, 0, -2, 0] }}
                transition={{ duration: 1.2, delay: 2, repeat: Infinity, repeatDelay: 5, ease: "easeInOut" }}
              >
                ?
              </motion.span>
            </h1>
            <p className="mt-3 text-sm font-medium tracking-widest" style={{ color: "var(--color-text-muted)" }}>
              SEARCH. TRANSCRIBE. LEARN.
            </p>
          </div>

          <div className="w-full">
            <SearchBar onSelect={handleSelect} />
          </div>

          {processing && (
            <div className="flex items-center gap-2 text-sm" style={{ color: "var(--color-accent-dim)" }}>
              <Loader2 size={16} className="animate-spin" />
              Processing song... this may take a few minutes.
            </div>
          )}

          {error && (
            <div className="w-full rounded-xl border px-5 py-3 text-sm" style={{ borderColor: "var(--color-border)", backgroundColor: "var(--color-bg-card)", color: "var(--color-danger)" }}>
              {error}
            </div>
          )}
        </div>
      </section>

      {hasSongs && (
        <section style={{ padding: "0 24px 64px" }}>
          <div className="mx-auto w-full max-w-lg">
            <h2 className="mb-4 text-xs font-semibold tracking-widest" style={{ color: "var(--color-text-muted)" }}>
              LIBRARY
            </h2>
            {isLoading ? (
              <div className="flex items-center gap-2 text-sm" style={{ color: "var(--color-text-muted)" }}>
                <Loader2 size={16} className="animate-spin" />
                Loading...
              </div>
            ) : (
              <div className="flex flex-col" style={{ gap: 12 }}>
                {songs.map((s) => (
                  <button key={s.id} onClick={() => navigate(`/song/${s.id}`)} className="w-full text-left">
                    <SongCard song={s} onDeleted={refetch} />
                  </button>
                ))}
              </div>
            )}
          </div>
        </section>
      )}
    </div>
  );
}
