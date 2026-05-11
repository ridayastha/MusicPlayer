import { useState, useEffect } from "react";

export default function EditMedicineModal({ medicine, onClose, onSave }) {
  const [form, setForm] = useState(medicine || {});
  const [errors, setErrors] = useState({});

  // Reset form whenever a new medicine is passed in
  useEffect(() => {
    if (medicine) {
      setForm(medicine);
      setErrors({});
    }
  }, [medicine]);

  if (!medicine) return null; // don't render if no medicine selected

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validate = () => {
    const newErrors = {};

    if (!form.med_name || form.med_name.trim() === "") {
      newErrors.med_name = "Medicine name is required";
    }

    if (form.stock === "" || form.stock < 0) {
      newErrors.stock = "Stock must be 0 or greater";
    }

    if (!form.expiry_date) {
      newErrors.expiry_date = "Expiry date is required";
    } else {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const expiry = new Date(form.expiry_date);
      expiry.setHours(0, 0, 0, 0);
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    onSave(form);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 className="text-lg font-bold mb-4">Edit Medicine</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Medicine Name */}
          <div>
            <input
              type="text"
              name="med_name"
              value={form.med_name || ""}
              onChange={handleChange}
              placeholder="Medicine Name"
              className="w-full border rounded p-2"
            />
            {errors.med_name && (
              <p className="text-red-600 text-sm mt-1">{errors.med_name}</p>
            )}
          </div>

          {/* Stock */}
          <div>
            <input
              type="number"
              name="stock"
              value={form.stock ?? ""}
              onChange={handleChange}
              placeholder="Stock"
              className="w-full border rounded p-2"
            />
            {errors.stock && (
              <p className="text-red-600 text-sm mt-1">{errors.stock}</p>
            )}
          </div>

          {/* Expiry Date */}
          <div>
            <input
              type="date"
              name="expiry_date"
              value={form.expiry_date || ""}
              onChange={handleChange}
              className="w-full border rounded p-2"
            />
            {errors.expiry_date && (
              <p className="text-red-600 text-sm mt-1">{errors.expiry_date}</p>
            )}
          </div>

          {/* Description */}
          <textarea
            name="description"
            value={form.description || ""}
            onChange={handleChange}
            placeholder="Description"
            className="w-full border rounded p-2"
          />

          {/* Buttons */}
          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded bg-slate-200 hover:bg-slate-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
