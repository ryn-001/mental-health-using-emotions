export default function ResponseBox({ data }) {
  if (!data) return null;

  return (
    <div className="card response">
      <h2>📊 Response</h2>

      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}