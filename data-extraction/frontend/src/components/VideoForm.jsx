import { useState } from "react";

export default function VideoForm({ onSubmit, loading }) {
  const [videoId, setVideoId] = useState("");

  return (
    <div className="card">
      <h2>🎥 YouTube Video</h2>

      <input
        className="input"
        placeholder="Enter Video ID (e.g. dQw4w9WgXcQ)"
        value={videoId}
        onChange={(e) => setVideoId(e.target.value)}
      />

      <button
        className="btn"
        onClick={() => onSubmit(videoId)}
        disabled={loading}
      >
        {loading ? "Extracting..." : "Extract Comments"}
      </button>
    </div>
  );
}