function RiskBadge({ risk }) {
  const colors = {
    Critical: "bg-red-600",
    High: "bg-orange-500",
    Medium: "bg-yellow-500 text-black",
    Low: "bg-green-600",
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-sm font-semibold ${
        colors[risk] || "bg-gray-600"
      }`}
    >
      {risk}
    </span>
  );
}

export default RiskBadge;