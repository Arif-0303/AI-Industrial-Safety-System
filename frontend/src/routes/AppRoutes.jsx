import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import SectorDetails from "../pages/SectorDetails/SectorDetails";
import IncidentHistory from "../pages/IncidentHistory/IncidentHistory";
import AIQuery from "../pages/AIQuery/AIQuery";
import Notifications from "../pages/notifications/Notifications";
import NotFound from "../pages/NotFound/NotFound";
import AIChat from "../pages/chat/AIChat";
function AppRoutes() {
  return (
    <Routes>

      <Route path="/" element={<Dashboard />} />

      <Route path="/login" element={<Login />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/sector/:id" element={<SectorDetails />} />

      <Route path="/incidents" element={<IncidentHistory />} />

      <Route path="/ai-query" element={<AIQuery />} />

      <Route
        path="/notifications"
        element={<Notifications />}
      />

      <Route path="*" element={<NotFound />} />
      <Route path="/chat" element={<AIChat />} />
    </Routes>
  );
}

export default AppRoutes;