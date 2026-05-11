import {Users, Activity, Calendar, HeartPulse, ShieldCheck, X, LineChartIcon, GridIcon} from "lucide-react";

export default function Sidebar({ isOpen, setIsOpen }) {
  const navItems = [
    { icon: <GridIcon size={20} />, label: "Dashboard", active: true },
    { icon: <LineChartIcon size={20} />, label: "Analytics" },
    { icon: <LineChartIcon size={20} />, label: "Settings" },
  ];

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40 lg:hidden" onClick={() => setIsOpen(false)} />
      )}

      <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r p-4 transform transition-transform duration-300 lg:static lg:translate-x-0 ${isOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <button onClick={() => setIsOpen(false)} className="lg:hidden absolute top-6 right-4 text-slate-400 hover:text-slate-600">
          {/*<X size={24} />*/}
        </button>

        <div className="flex items-center gap-3 mb-10">
          <div className="bg-indigo-800 p-2 rounded text-white ">
            <HeartPulse size={24} />
          </div>
          <h6 className="font-bold tracking-tight ">Patient Management System</h6>
        </div>

        <nav className="space-y-3">
          {navItems.map((item) => (
            <div
              key={item.label}
              className={`flex items-center gap-3 px-4 py-4 rounded cursor-pointer transition-colors ${item.active ? "bg-blue-50 text-blue-600 font-semibold" : "text-slate-500 hover:bg-slate-50"}`}
            >
              {item.icon} <span className="text-sm">{item.label}</span>
            </div>
          ))}
        </nav>

        {/*<div className="mt-5 p-4 bg-slate-50 rounded-2xl border flex items-center gap-2 text-emerald-600">*/}
        {/*  <ShieldCheck size={16} />*/}
        {/*  <span className="text-[10px] font-bold uppercase tracking-widest">HIPAA Secure</span>*/}
        {/*</div>*/}
      </aside>
    </>
  );
}