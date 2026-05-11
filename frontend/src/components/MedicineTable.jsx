import {Pencil, Trash2} from "lucide-react";

export default function MedicineTable({ medicines = [], onDelete, onEdit }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-center">
        <thead className="bg-white border-b text-slate-500 font-semibold uppercase text-[11px] tracking-wider">
          <tr>
            <th className="p-4 text-left">Medicine</th>
            <th className="p-4">Stock</th>
            <th className="p-4">Expiry Date</th>
            <th className="p-4">Status</th>
            <th className="p-4">Action</th>
          </tr>
        </thead>

        <tbody>
          {medicines.length === 0 ? (
            <tr>
              <td colSpan="5" className="p-10 text-slate-400 italic">
                No medicines available
              </td>
            </tr>
          ) : (
            medicines.map((m) => {
              const isLowStock = (m.stock ?? 0) <= 10;

              // Normalize dates to midnight for reliable comparison
              const today = new Date();
              today.setHours(0, 0, 0, 0);

              const expiry = m.expiry_date ? new Date(m.expiry_date) : null;
              if (expiry) expiry.setHours(0, 0, 0, 0);

              const isExpired = expiry && expiry <= today;

              const daysUntilExpiry = expiry
                ? Math.ceil((expiry - today) / (1000 * 60 * 60 * 24))
                : null;

              const isExpiringSoon =
                daysUntilExpiry !== null && daysUntilExpiry <= 30;

              return (
                <tr
                  key={m.id}
                  className={`border-b hover:bg-slate-50 transition ${
                    isExpired
                      ? "bg-red-50"
                      : isExpiringSoon
                      ? "bg-yellow-50"
                      : ""
                  }`}
                >
                  {/* Medicine Name */}
                  <td className="p-4 text-left font-semibold text-slate-700">
                    {m.med_name || "Unknown"}
                  </td>

                  {/* Stock */}
                  <td className="p-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-bold ${
                        isLowStock
                          ? "bg-red-100 text-red-600"
                          : "bg-green-100 text-green-600"
                      }`}
                    >
                      {m.stock ?? 0}
                    </span>
                  </td>

                  {/* Expiry Date */}
                  <td className="p-4 text-slate-500">
                    {m.expiry_date
                      ? new Date(m.expiry_date).toLocaleDateString("en-GB")
                      : "N/A"}
                  </td>

                  {/* Status */}
                  <td className="p-4">
                    <span
                      className={`text-xs font-bold ${
                        isExpired
                          ? "text-red-600"
                          : isExpiringSoon
                          ? "text-yellow-600"
                          : "text-green-600"
                      }`}
                    >
                      {isExpired
                        ? "Expired"
                        : isExpiringSoon
                        ? "Expiring Soon"
                        : "Active"}
                    </span>
                  </td>

                  {/* Action */}
                  <td className="p-4">
                    <button
                      onClick={() => onDelete(m.id)}
                      className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition"
                      aria-label="Delete medicine"
                    >
                      <Trash2 size={18} />
                    </button>
                    <button
                        onClick={() => onEdit(m.id)}
                        className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                        aria-label="Edit patient"
                      >
                        <Pencil size={18} />
                      </button>
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
