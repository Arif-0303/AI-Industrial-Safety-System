import { useEffect } from "react";

function NotificationToast({
  notification,
  onClose,
}) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 4000);

    return () => clearTimeout(timer);
  }, [onClose]);

  const bgColor = {
    danger: "bg-red-600",
    warning: "bg-yellow-500",
    info: "bg-blue-600",
    safe: "bg-green-600",
  };

  return (
    <div
      className={`${bgColor[notification.severity?.toLowerCase()] || "bg-slate-800"}
      text-white
      p-4
      rounded-lg
      shadow-2xl
      w-96
      animate-pulse`}
    >
      <h3 className="font-bold text-lg">
        {notification.title}
      </h3>

      <p className="mt-2">
        {notification.message}
      </p>
    </div>
  );
}

export default NotificationToast;