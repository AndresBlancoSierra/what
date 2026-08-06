import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import SongPage from "./pages/SongPage";

export default function App() {
  return (
    <div className="min-h-dvh bg-bg text-text">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/song/:id" element={<SongPage />} />
      </Routes>
    </div>
  );
}
