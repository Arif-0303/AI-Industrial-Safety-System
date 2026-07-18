import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Factory,
  History,
  MessageSquare,
  Building2,
} from "lucide-react";

function Sidebar() {
  const menu = [
    {
      title: "Dashboard",
      path: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      title: "🏭 Sections",
      path: "/sections",
      icon: Building2,
    },
    {
      title: "Sector Details",
      path: "/sector/1",
      icon: Factory,
    },
    {
      title: "Incident History",
      path: "/incidents",
      icon: History,
    },
    {
      title: "AI Query",
      path: "/ai-query",
      icon: MessageSquare,
    },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-bold text-red-500">
          AI Safety
        </h1>

        <p className="text-sm text-slate-400 mt-1">
          Industrial Control
        </p>
      </div>

      <nav className="flex-1 p-4">
        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.title}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition ${
                  isActive
                    ? "bg-red-600 text-white"
                    : "hover:bg-slate-800 text-slate-300"
                }`
              }
            >
              <Icon size={20} />
              {item.title}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;