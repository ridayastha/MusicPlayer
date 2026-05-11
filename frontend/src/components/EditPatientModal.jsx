import { useState, useEffect } from "react";

export default function EditPatientModal({ patient, onClose, onSave }) {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    date_of_birth: "",
    email: "",
    gender: "",
  });
  const [errors, setErrors] = useState({});

  // Initialize form when patient changes
  useEffect(() => {
    if (patient) {
      setFormData({
        first_name: patient.first_name || "",
        last_name: patient.last_name || "",
        date_of_birth: patient.date_of_birth || "",
        email: patient.email || "",
        gender: patient.gender || "",
      });
    }
  }, [patient]);

  const validate = () => {
    const newErrors = {};
    if (!formData.first_name.trim()) newErrors.first_name = "First name required";
    if (!formData.last_name.trim()) newErrors.last_name = "Last name required";
    if (!formData.date_of_birth) newErrors.date_of_birth = "Date of birth required";
    if (!formData.email.trim()) newErrors.email = "Email required";
    if (!formData.gender) newErrors.gender = "Gender required";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    if (!validate()) return;
    onSave({ ...patient, ...formData });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-lg p-6 w-[400px]">
        <h2 className="text-lg font-bold mb-4">Edit Patient</h2>

        <div className="space-y-3">
          {/* First Name */}
          <div>
            <label className="block text-sm font-medium">First Name</label>
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              className="border rounded w-full p-2"
            />
            {errors.first_name && <p className="text-red-500 text-xs">{errors.first_name}</p>}
          </div>

          {/* Last Name */}
          <div>
            <label className="block text-sm font-medium">Last Name</label>
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              className="border rounded w-full p-2"
            />
            {errors.last_name && <p className="text-red-500 text-xs">{errors.last_name}</p>}
          </div>

          {/* Date of Birth */}
          <div>
            <label className="block text-sm font-medium">Date of Birth</label>
            <input
              type="date"
              name="date_of_birth"
              value={formData.date_of_birth}
              onChange={handleChange}
              className="border rounded w-full p-2"
            />
            {errors.date_of_birth && <p className="text-red-500 text-xs">{errors.date_of_birth}</p>}
          </div>

          {/* Email */}
          <div>
            <label className="block text-sm font-medium">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="border rounded w-full p-2"
            />
            {errors.email && <p className="text-red-500 text-xs">{errors.email}</p>}
          </div>

          {/* Gender */}
          <div>
            <label className="block text-sm font-medium">Gender</label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="border rounded w-full p-2"
            >
              <option value="">Select gender</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </select>
            {errors.gender && <p className="text-red-500 text-xs">{errors.gender}</p>}
          </div>
        </div>

        <div className="flex justify-end gap-2 mt-4">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
