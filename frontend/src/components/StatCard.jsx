export default function StatCard({ label, value, icon }) {
  return (
    <div className="bg-white p-6 border border-slate-200">
      <div className="mb-3">{icon}</div>
      <p className="text-slate-500 text-sm">{label}</p>
      <h3 className="text-2xl font-bold">{value}</h3>
    </div>
  );
}