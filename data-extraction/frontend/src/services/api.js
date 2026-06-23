export async function extractComments(videoId, groupName) {
  const res = await fetch("http://localhost:5000/extract-comments", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_id: videoId,
      group_name: groupName,
    }),
  });

  return await res.json();
}