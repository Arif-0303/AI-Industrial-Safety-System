import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";

function TemperatureChart({ sectors }) {
  if (!sectors || sectors.length === 0) return null;

  return (
    <div className="bg-slate-800 rounded-xl p-5">
      <h2 className="text-xl font-bold mb-4 text-white">
        Live Temperature Monitoring
      </h2>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={sectors}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="name"
            stroke="#ffffff"
          />

          <YAxis
            stroke="#ffffff"
          />

          <Tooltip />

          <Bar
            dataKey="temperature"
            fill="#ef4444"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TemperatureChart;