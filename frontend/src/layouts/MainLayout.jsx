import Sidebar from "../components/sidebar/Sidebar";
import Navbar from "../components/navbar/Navbar";

function MainLayout({ children }) {
  return (
    <div className="flex h-screen bg-slate-950 text-white">

      <Sidebar />

      <div className="flex flex-col flex-1 overflow-hidden">

        <Navbar />

        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>

      </div>

    </div>
  );
}

export default MainLayout;