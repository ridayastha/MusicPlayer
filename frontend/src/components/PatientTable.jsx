import { Trash2, Pencil } from "lucide-react"; // Added Pencil icon

export default function PatientTable({ patients = [], loading, onDelete, onEdit }) {
  if (loading) {
    return (
      <div className="p-10 text-center text-slate-400 animate-pulse">
        Loading patients...
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-center">
        <thead className="bg-white border-b text-slate-500 font-semibold uppercase text-[11px] tracking-wider">
          <tr>
            <th className="p-4 text-left">Patient</th>
            <th className="p-4">Gender</th>
            <th className="p-4">Date of Birth</th>
            <th className="p-4">Email</th>
            <th className="p-4 text-right pr-8">Action</th>
          </tr>
        </thead>

        <tbody>
          {patients.length === 0 ? (
            <tr>
              <td colSpan="5" className="p-10 text-slate-400 italic">
                No patients found
              </td>
            </tr>
          ) : (
            patients.map((p) => {
              const first = p.first_name?.[0] || "?";
              const last = p.last_name?.[0] || "?";

              return (
                <tr key={p.id} className="border-b hover:bg-slate-50 transition">
                  {/* Patient Info */}
                  <td className="p-4 text-left font-semibold text-slate-700">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-blue-100 text-blue-600 flex items-center justify-center rounded-full text-[10px] font-bold uppercase">
                        {first}{last}
                      </div>
                      <span>
                        {p.first_name || "Unknown"} {p.last_name || ""}
                      </span>
                    </div>
                  </td>

                  {/* Gender Tag */}
                  <td className="p-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      p.gender === "M"
                        ? "bg-blue-50 text-blue-600"
                        : p.gender === "F"
                        ? "bg-rose-50 text-rose-600"
                        : "bg-green-50 text-green-600"
                    }`}>
                      {p.gender === "M" ? "Male" : p.gender === "F" ? "Female" : "Other"}
                    </span>
                  </td>

                  {/* DOB */}
                  <td className="p-4 text-slate-500">
                    {p.date_of_birth
                      ? new Date(p.date_of_birth).toLocaleDateString()
                      : "N/A"}
                  </td>

                  {/* Email */}
                  <td className="p-4 text-slate-500">
                    {p.email || "N/A"}
                  </td>

                  {/* Enhanced Action Column */}
                  <td className="p-4 text-right pr-4">
                    <div className="flex justify-end gap-1">

                      <button
                        onClick={() => onDelete(p.id)}
                        className="p-2 text-red-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                        aria-label="Delete patient"
                      >
                        <Trash2 size={18} />
                      </button>
                      <button
                        onClick={() => onEdit(p.id)}
                        className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                        aria-label="Edit patient"
                      >
                        <Pencil size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}