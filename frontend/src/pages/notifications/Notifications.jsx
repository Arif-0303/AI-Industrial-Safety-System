import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [filter, setFilter] = useState("All");

  const loadNotifications = async () => {
    try {
      const res = await axios.get(`${API}/notifications/`);
      setNotifications(res.data.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadNotifications();

    const interval = setInterval(loadNotifications, 5000);

    return () => clearInterval(interval);
  }, []);

  const markRead = async (id) => {
    try {
      await axios.put(`${API}/notifications/${id}/read`);
      loadNotifications();
    } catch (err) {
      console.error(err);
    }
  };

  const deleteNotification = async (id) => {
    try {
      await axios.delete(`${API}/notifications/${id}`);
      loadNotifications();
    } catch (err) {
      console.error(err);
    }
  };

  const filtered =
    filter === "All"
      ? notifications
      : notifications.filter(
          (n) => n.severity.toLowerCase() === filter.toLowerCase()
        );

  return (
    <div className="p-8">

      <h1 className="text-3xl font-bold mb-6">
        Notifications
      </h1>

      <div className="flex gap-3 mb-6">

        <button
          onClick={() => setFilter("All")}
          className="px-4 py-2 bg-gray-700 text-white rounded"
        >
          All
        </button>

        <button
          onClick={() => setFilter("Danger")}
          className="px-4 py-2 bg-red-600 text-white rounded"
        >
          Danger
        </button>

        <button
          onClick={() => setFilter("Warning")}
          className="px-4 py-2 bg-yellow-500 text-white rounded"
        >
          Warning
        </button>

        <button
          onClick={() => setFilter("Info")}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Info
        </button>

      </div>

      {filtered.length === 0 ? (
        <div className="text-gray-500">
          No Notifications
        </div>
      ) : (
        filtered.map((item) => (
          <div
            key={item.id}
            className="bg-white shadow rounded-lg p-5 mb-4"
          >
            <div className="flex justify-between">

              <div>

                <h2 className="font-bold text-lg">
                  {item.title}
                </h2>

                <p>{item.message}</p>

                <p className="text-sm mt-2">
                  Severity :
                  <b> {item.severity}</b>
                </p>

                <p className="text-sm">
                  Sector :
                  <b> {item.sector}</b>
                </p>

                <p className="text-xs text-gray-500 mt-2">
                  {item.created_at}
                </p>

              </div>

              <div className="flex flex-col gap-2">

                {!item.is_read && (
                  <button
                    onClick={() => markRead(item.id)}
                    className="bg-green-600 text-white px-3 py-1 rounded"
                  >
                    Mark Read
                  </button>
                )}

                <button
                  onClick={() => deleteNotification(item.id)}
                  className="bg-red-600 text-white px-3 py-1 rounded"
                >
                  Delete
                </button>

              </div>

            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default Notifications;