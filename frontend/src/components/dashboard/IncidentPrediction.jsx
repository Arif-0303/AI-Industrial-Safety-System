function IncidentPrediction({ sectors }) {
  return (
    <div className="bg-white rounded-xl shadow-md p-5 mt-8">

      <h2 className="text-2xl font-bold mb-4">
        AI Incident Prediction
      </h2>

      <div className="overflow-x-auto">

        <table className="min-w-full border">

          <thead className="bg-gray-100">

            <tr>
              <th className="border px-4 py-2">Sector</th>
              <th className="border px-4 py-2">Probability</th>
              <th className="border px-4 py-2">Severity</th>
              <th className="border px-4 py-2">Cause</th>
              <th className="border px-4 py-2">Recommendation</th>
            </tr>

          </thead>

          <tbody>

            {sectors.map((sector) => {

              const prediction = sector.incident_prediction;

              if (!prediction) return null;

              return (

                <tr key={sector.sector_id || sector.id}>

                  <td className="border px-4 py-2">
                    {sector.sector_name || sector.name}
                  </td>

                  <td className="border px-4 py-2">
                    {prediction.accident_probability}%
                  </td>

                  <td
                    className={`border px-4 py-2 font-semibold
                    ${
                      prediction.severity === "Critical"
                        ? "text-red-600"
                        : prediction.severity === "High"
                        ? "text-orange-600"
                        : prediction.severity === "Medium"
                        ? "text-yellow-600"
                        : "text-green-600"
                    }`}
                  >
                    {prediction.severity}
                  </td>

                  <td className="border px-4 py-2">
                    {prediction.cause}
                  </td>

                  <td className="border px-4 py-2">
                    {prediction.recommendation}
                  </td>

                </tr>

              );

            })}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default IncidentPrediction;