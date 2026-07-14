import { useEffect, useState } from "react";
import { Bell, UserCircle } from "lucide-react";
import { Link } from "react-router-dom";
import axios from "axios";

import websocketService from "../../services/websocketService";

function Navbar() {
  const [notifications, setNotifications] = useState([]);
  const [showPanel, setShowPanel] = useState(false);

  const loadNotifications = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/notifications/"
      );

      setNotifications(res.data.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadNotifications();

    websocketService.connect();

    websocketService.onNotification((notification) => {
      setNotifications((prev) => {
        const exists = prev.find(
          (item) =>
            item.title === notification.title &&
            item.message === notification.message
        );

        if (exists) return prev;

        return [
          {
            id: Date.now(),
            title: notification.title,
            message: notification.message,
            severity: notification.severity || "Info",
            is_read: false,
          },
          ...prev,
        ];
      });
    });

    return () => {};
  }, []);

  const unread = notifications.filter(
    (item) => !item.is_read
  ).length;

  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6 relative">
      <div>
        <h2 className="text-2xl font-bold text-white">
          Industrial Safety Dashboard
        </h2>
      </div>

      <div className="flex items-center gap-6">

        {/* Notification Bell */}
        <div className="relative">
          <button
            onClick={() => setShowPanel(!showPanel)}
            className="relative"
          >
            <Bell className="cursor-pointer text-white" />

            {unread > 0 && (
              <span className="absolute -top-2 -right-2 bg-red-600 text-white rounded-full h-5 w-5 text-xs flex items-center justify-center">
                {unread}
              </span>
            )}
          </button>

          {showPanel && (
            <div className="absolute right-0 mt-4 w-96 bg-white text-black rounded-lg shadow-2xl border border-gray-300 z-50 max-h-96 overflow-y-auto">

              <div className="p-4 border-b border-gray-200 bg-gray-100">
                <h3 className="font-bold text-lg text-black">
                  Notifications
                </h3>
              </div>

              {notifications.length === 0 ? (
                <div className="p-6 text-center text-gray-600">
                  No Notifications
                </div>
              ) : (
                notifications.slice(0, 5).map((item) => (
                  <div
                    key={item.id}
                    className="border-b border-gray-200 p-4 hover:bg-gray-100 transition"
                  >
                    <h4 className="font-bold text-black">
                      {item.title}
                    </h4>

                    <p className="text-sm text-gray-700 mt-1">
                      {item.message}
                    </p>

                    <span
                      className={`inline-block mt-2 text-xs font-bold px-2 py-1 rounded ${
                        item.severity?.toLowerCase() === "danger"
                          ? "bg-red-100 text-red-700"
                          : item.severity?.toLowerCase() === "warning"
                          ? "bg-yellow-100 text-yellow-700"
                          : item.severity?.toLowerCase() === "safe"
                          ? "bg-green-100 text-green-700"
                          : "bg-blue-100 text-blue-700"
                      }`}
                    >
                      {item.severity}
                    </span>
                  </div>
                ))
              )}

              <Link
                to="/notifications"
                className="block text-center p-3 bg-slate-900 text-white hover:bg-slate-800"
              >
                View All Notifications
              </Link>
            </div>
          )}
        </div>

        {/* User */}
        <div className="flex items-center gap-2 text-white">
          <UserCircle size={30} />
          <span>Admin</span>
        </div>
      </div>
    </header>
  );
}

export default Navbar;