import { useState } from "react";
import { Search, Loader2 } from "lucide-react";
import type { SearchResult } from "../api/client";
import { searchSongs } from "../api/client";

interface Props {
  onSelect: (result: SearchResult) => void;
}

export default function SearchBar({ onSelect }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch() {
    if (!query.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await searchSongs(query);
      setResults(res);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <div style={{ position: "relative", display: "flex", alignItems: "center" }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Search for a song..."
          style={{
            width: "100%",
            padding: "16px 56px 16px 20px",
            fontSize: 15,
            borderRadius: 9999,
            border: "1px solid var(--color-border)",
            backgroundColor: "var(--color-bg-card)",
            color: "var(--color-text)",
            outline: "none",
          }}
          onFocus={(e) => { e.target.style.borderColor = "var(--color-border-hover)"; }}
          onBlur={(e) => { e.target.style.borderColor = "var(--color-border)"; }}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          style={{
            position: "absolute",
            right: 6,
            width: 40,
            height: 40,
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            border: "none",
            cursor: "pointer",
            backgroundColor: "var(--color-accent)",
            color: "var(--color-bg)",
            opacity: loading ? 0.5 : 1,
          }}
        >
          {loading ? (
            <Loader2 size={18} className="animate-spin" />
          ) : (
            <Search size={18} />
          )}
        </button>
      </div>

      {error && (
        <p style={{ fontSize: 14, color: "var(--color-danger)" }}>{error}</p>
      )}

      {results.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <p style={{ fontSize: 12, fontWeight: 600, letterSpacing: "0.05em", color: "var(--color-text-muted)" }}>
            RESULTS
          </p>
          {results.map((r, i) => (
            <button
              key={i}
              onClick={() => onSelect(r)}
              style={{
                width: "100%",
                padding: 16,
                borderRadius: 12,
                border: "1px solid var(--color-border)",
                backgroundColor: "var(--color-bg-card)",
                color: "var(--color-text)",
                textAlign: "left",
                cursor: "pointer",
                transition: "all 0.15s",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = "var(--color-border-hover)";
                e.currentTarget.style.backgroundColor = "var(--color-bg-hover)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = "var(--color-border)";
                e.currentTarget.style.backgroundColor = "var(--color-bg-card)";
              }}
            >
              <p style={{ fontWeight: 500 }}>{r.full_title}</p>
              <p style={{ marginTop: 4, fontSize: 14, color: "var(--color-text-secondary)" }}>
                {r.artist} &middot; {r.duration ? `${Math.round(r.duration / 60)}m` : "?"}
              </p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
