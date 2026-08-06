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
