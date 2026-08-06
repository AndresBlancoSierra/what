import { useState } from "react";
import { Download } from "lucide-react";

interface Props {
  songId: string;
  onExport: () => Promise<void>;
}

export default function ExportButton({ songId, onExport }: Props) {
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState("");

  async function handleExport() {
    setLoading(true);
    setError("");
    try {
      await onExport();
      setDone(true);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="shrink-0">
      <button
        onClick={handleExport}
        disabled={loading}
        className="flex items-center gap-2 rounded-full border border-border bg-bg-card px-4 py-2 text-sm font-medium text-text-secondary transition hover:border-border-hover hover:text-text disabled:opacity-50"
      >
        <Download size={16} />
        {loading ? "Exporting..." : done ? "Exported!" : "Export to Anki"}
      </button>
      {error && <p className="mt-1 text-xs text-danger">{error}</p>}
    </div>
  );
}
