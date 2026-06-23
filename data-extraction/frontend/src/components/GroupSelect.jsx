export default function GroupSelect({ group, setGroup }) {
  return (
    <div className="card">
      <h2>🧠 Mental Health Group</h2>

      <select
        className="input"
        value={group}
        onChange={(e) => setGroup(e.target.value)}
      >
        <option>Anxiety</option>
        <option>Depression</option>
        <option>Loneliness</option>
        <option>Isolation</option>
        <option>Stress</option>
        <option>Recovery</option>
        <option>Wellbeing</option>
      </select>
    </div>
  );
}