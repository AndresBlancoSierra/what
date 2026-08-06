const BASE = "/api";

export interface SearchResult {
  title: string;
  artist: string;
  url: string;
  duration: number;
  full_title: string;
}

export interface SongSummary {
  id: string;
  title: string;
  artist: string;
  duration: number;
  segments_count: number;
  created_at: string;
}

export interface Segment {
  id: number;
  line_number: number;
  text: string;
  start_time: number;
  end_time: number;
}

export interface SongDetail {
  id: string;
  title: string;
  artist: string;
  youtube_url: string;
  audio_path: string;
  duration: number;
  lyrics_text: string;
  created_at: string;
  segments: Segment[];
}

export async function searchSongs(query: string): Promise<SearchResult[]> {
  const res = await fetch(`${BASE}/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error("Search failed");
  const data = await res.json();
  return data.results;
}

export async function processSong(youtube_url: string, title: string, artist: string): Promise<SongSummary> {
  const res = await fetch(`${BASE}/songs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ youtube_url, title, artist }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Processing failed");
  }
  return res.json();
}

export async function listSongs(): Promise<SongSummary[]> {
  const res = await fetch(`${BASE}/songs`);
  if (!res.ok) throw new Error("Failed to fetch songs");
  const data = await res.json();
  return data.songs;
}

export async function getSong(id: string): Promise<SongDetail> {
  const res = await fetch(`${BASE}/songs/${id}`);
  if (!res.ok) throw new Error("Song not found");
  return res.json();
}

export function getAudioUrl(id: string): string {
  return `${BASE}/songs/${id}/audio`;
}

export async function deleteSong(id: string): Promise<void> {
  const res = await fetch(`${BASE}/songs/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Delete failed");
}

export async function exportSong(id: string): Promise<{ export_path: string; segments_count: number }> {
  const res = await fetch(`${BASE}/songs/${id}/export`, { method: "POST" });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Export failed");
  }
  return res.json();
}
