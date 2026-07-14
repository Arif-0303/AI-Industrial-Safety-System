function PlantHealthCard({ sectors }) {
  const healthy = sectors.filter(
    (sector) => sector.risk_level === "Safe"
  ).length;

  return (
    <div className="bg-slate-800 rounded-xl p-5 shadow-lg">
      <h3 className="text-gray-400 text-sm">Plant Health</h3>

      <p className="text-3xl font-bold text-green-400 mt-2">
        {healthy}/{sectors.length}
      </p>

      <p className="text-sm text-gray-500 mt-2">
        Safe Sectors
      </p>
    </div>
  );
}

export default PlantHealthCard;