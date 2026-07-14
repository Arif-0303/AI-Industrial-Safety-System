import { useEffect, useState } from "react";
import { getSectors } from "../../services/sectorService";
import websocketService from "../../services/websocketService";
import NotificationToast from "../../components/notifications/NotificationToast";
import PlantHealthCard from "../../components/stats/PlantHealthCard";
import ActiveAlertCard from "../../components/stats/ActiveAlertCard";
import WorkerCard from "../../components/stats/WorkerCard";
import RiskScoreCard from "../../components/stats/RiskScoreCard";

import TemperatureChart from "../../components/charts/TemperatureChart";

import MainLayout from "../../layouts/MainLayout";
import LiveAlerts from "../../components/dashboard/LiveAlerts";
import DashboardLayout from "../../components/dashboard/DashboardLayout";
import SectionTitle from "../../components/dashboard/SectionTitle";
import PlantStatus from "../../components/dashboard/PlantStatus";
import PlantOverview from "../../components/dashboard/PlantOverview";
import SectorGrid from "../../components/dashboard/SectorGrid";

function Dashboard() {
  const [sectors, setSectors] = useState([]);
  const [wsStatus, setWsStatus] = useState("Disconnected");
  const [lastMessage, setLastMessage] = useState(null);
  const [toast, setToast] = useState(null);
  // Initial API Load
  const loadSectors = async () => {
    try {
      const data = await getSectors();
      setSectors(data);
    } catch (error) {
      console.error("Failed to fetch sectors:", error);
    }
  };

  useEffect(() => {
    // Load initial data once
    loadSectors();

    // Connect WebSocket
    websocketService.connect();
    websocketService.onNotification((notification) => {
  setToast(notification);
  });
    setWsStatus("Connected");

    // Listen for Live Updates
    websocketService.onMessage((message) => {
      console.log("Live WebSocket:", message);

      setLastMessage(message);

      // Update Dashboard automatically
      if (
        message.type === "sensor_update" &&
        Array.isArray(message.data)
      ) {
        setSectors(
          message.data.map((item) => ({
            id: item.sector_id,
            name: item.sector_name,
            temperature: item.temperature,
            gas: item.gas,
            pressure: item.pressure,
            workers_present: item.workers_present,
            maintenance: item.maintenance,
            risk_score: item.risk_score,
            ml_prediction: item.ml_prediction,
            recommendation: item.recommendation,
            alerts: item.alerts,
            predictive_maintenance: item.predictive_maintenance,
            incident_prediction: item.incident_prediction,
      }))
    );
 }

      // Single sector update
      if (
        message.type === "sector_update" &&
        message.data
      ) {
        setSectors((prev) =>
          prev.map((sector) =>
            sector.id === message.data.sector_id
              ? {
                  ...sector,
                  temperature: message.data.temperature,
                  gas: message.data.gas,
                  pressure: message.data.pressure,
                  workers_present: message.data.workers_present,
                  maintenance: message.data.maintenance,
                  risk_score: message.data.risk_score,
                }
              : sector
          )
        );
      }
    });

    return () => {
      websocketService.disconnect();
      setWsStatus("Disconnected");
    };
  }, []);

  return (
    <MainLayout>
      <DashboardLayout>

        <SectionTitle
          title="Industrial Safety Dashboard"
          subtitle="Real-Time Monitoring & AI Risk Assessment"
        />

        {/* WebSocket Status */}
        <div className="flex justify-end mb-4">
          <div className="rounded-lg bg-gray-800 px-4 py-2 text-sm text-white">
            WebSocket :
            <span
              className={`ml-2 font-semibold ${
                wsStatus === "Connected"
                  ? "text-green-400"
                  : "text-red-400"
              }`}
            >
              {wsStatus}
            </span>
          </div>
        </div>

      

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
          <PlantHealthCard sectors={sectors} />
          <ActiveAlertCard sectors={sectors} />
          <WorkerCard sectors={sectors} />
          <RiskScoreCard sectors={sectors} />
        </div>

        <PlantOverview sectors={sectors} />

        <div className="mt-8 mb-8">
          <TemperatureChart sectors={sectors} />
        </div>

        <LiveAlerts sectors={sectors} />

        {lastMessage && (
          <div className="mb-8 rounded-lg bg-gray-900 p-4 text-white">
            <h3 className="mb-2 text-lg font-semibold">
              Live WebSocket Message
            </h3>

            <pre className="overflow-auto text-sm">
              {JSON.stringify(lastMessage, null, 2)}
            </pre>
          </div>
        )}

        <div>
          <h2 className="text-2xl font-bold mb-6">
            Production Sectors
          </h2>

          <SectorGrid sectors={sectors} />
        </div>

      </DashboardLayout>
    {toast && (
  <div className="fixed top-5 right-5 z-50">
    <NotificationToast
      notification={toast}
      onClose={() => setToast(null)}
    />
  </div>
)}
    </MainLayout>
  );
}

export default Dashboard;