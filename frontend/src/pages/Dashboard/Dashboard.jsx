import { useEffect, useState } from "react";
import { getSectors } from "../../services/sectorService";
import websocketService from "../../services/websocketService";
import NotificationToast from "../../components/notifications/NotificationToast";
import PlantHealthCard from "../../components/stats/PlantHealthCard";
import ActiveAlertCard from "../../components/stats/ActiveAlertCard";
import WorkerCard from "../../components/stats/WorkerCard";
import RiskScoreCard from "../../components/stats/RiskScoreCard";
import IncidentPredictionCard from "../../components/stats/IncidentPredictionCard";
import EmergencyPopup from "../../components/dashboard/EmergencyPopup";
import TemperatureChart from "../../components/charts/TemperatureChart";
import EmergencyOverlay from "../../components/dashboard/EmergencyOverlay";
import MainLayout from "../../layouts/MainLayout";
import LiveAlerts from "../../components/dashboard/LiveAlerts";
import DashboardLayout from "../../components/dashboard/DashboardLayout";
import SectionTitle from "../../components/dashboard/SectionTitle";
import PlantOverview from "../../components/dashboard/PlantOverview";
import SectorGrid from "../../components/dashboard/SectorGrid";
import DigitalTwin from "../../components/dashboard/DigitalTwin";
import ActionLog from "../../components/dashboard/ActionLog";
import CommandCenter from "../../components/dashboard/CommandCenter";
import StartMonitoring from "../../components/dashboard/StartMonitoring";

function Dashboard() {
  const [sectors, setSectors] = useState([]);
  const [wsStatus, setWsStatus] = useState("Disconnected");
  const [lastMessage, setLastMessage] = useState(null);
  const [toast, setToast] = useState(null);
  const [emergency, setEmergency] = useState(null);
  const [emergencyMode, setEmergencyMode] = useState(false);
  const [actionLogs, setActionLogs] = useState([]);
  const [systemStarted, setSystemStarted] = useState(false);

  // Initial API Load
  const loadSectors = async () => {
    try {
      const data = await getSectors();
      setSectors(data);
    } catch (error) {
      console.error("Failed to fetch sectors:", error);
    }
  };

  const addActionLog = (log) => {
    setActionLogs((prev) => [log, ...prev]);
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

      // Full sensor update
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

        // Find highest priority emergency
        const criticalSector = [...message.data]
          .filter(
            (sector) =>
              sector.risk_score >= 80 &&
              sector.workers_present > 0
          )
          .sort((a, b) => b.risk_score - a.risk_score)[0];

        if (criticalSector) {
          setEmergency(criticalSector);
        } else {
          setEmergency(null);
          setEmergencyMode(false);
        }
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

  // ============================
  // Start Monitoring Screen
  // ============================
  if (!systemStarted) {
    return (
      <StartMonitoring
        onStart={() => {
          setSystemStarted(true);
        }}
      />
    );
  }

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

        {/* Dashboard Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-6 mb-8">
          <PlantHealthCard sectors={sectors} />
          <ActiveAlertCard sectors={sectors} />
          <WorkerCard sectors={sectors} />
          <RiskScoreCard sectors={sectors} />
          <IncidentPredictionCard sectors={sectors} />
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

        <DigitalTwin sectors={sectors} />
      </DashboardLayout>

      {toast && (
        <div className="fixed top-5 right-5 z-50">
          <NotificationToast
            notification={toast}
            onClose={() => setToast(null)}
          />
        </div>
      )}

      <EmergencyPopup
        emergency={emergency}
        onBroadcast={() => {
          console.log("Emergency Broadcast Started");
          setEmergencyMode(true);
        }}
        onClose={() => {
          setEmergency(null);
          setEmergencyMode(false);
          setActionLogs([]);
        }}
      />

      <CommandCenter
        emergency={emergency}
        onLog={addActionLog}
      />

      <ActionLog logs={actionLogs} />

      <EmergencyOverlay
        open={emergencyMode}
        emergency={emergency}
      />
    </MainLayout>
  );
}

export default Dashboard;