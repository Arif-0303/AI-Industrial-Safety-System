function InfoCard({ title, value, color = "text-white" }) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
      <p className="text-slate-400 text-sm">{title}</p>

      <h2 className={`text-2xl font-bold mt-2 ${color}`}>
        {value}
      </h2>
    </div>
  );
}

export default InfoCard;