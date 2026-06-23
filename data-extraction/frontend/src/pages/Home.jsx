import { useState } from "react";
import VideoForm from "../components/VideoForm";
import GroupSelect from "../components/GroupSelect";
import ResponseBox from "../components/ResponseBox";
import { extractComments } from "../services/api";

export default function Home() {
  const [group, setGroup] = useState("Depression");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleSubmit = async (videoId) => {
    if (!videoId) return;

    setLoading(true);
    setResponse(null);

    const data = await extractComments(videoId, group);

    setResponse(data);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">🧠 Mental Health Data Extractor</h1>

      <div className="grid">
        <VideoForm onSubmit={handleSubmit} loading={loading} />
        <GroupSelect group={group} setGroup={setGroup} />
      </div>

      <ResponseBox data={response} />
    </div>
  );
}