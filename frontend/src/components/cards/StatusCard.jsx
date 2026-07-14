function StatusCard({ title, value, color }) {
  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
      <p className="text-slate-400">{title}</p>

      <h2 className={`text-4xl font-bold mt-3 ${color}`}>
        {value}
      </h2>
    </div>
  );
}

export default StatusCard;