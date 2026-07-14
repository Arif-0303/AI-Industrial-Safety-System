function ActiveAlertCard({ sectors }) {

  let alerts = 0;

  sectors.forEach((sector) => {
    alerts += sector.alerts.length;
  });

  return (
    <div className="bg-slate-800 rounded-xl p-5 shadow-lg">

      <h3 className="text-gray-400 text-sm">
        Active Alerts
      </h3>

      <p className="text-3xl font-bold text-red-400 mt-2">
        {alerts}
      </p>

      <p className="text-sm text-gray-500 mt-2">
        Current Alerts
      </p>

    </div>
  );
}

export default ActiveAlertCard;