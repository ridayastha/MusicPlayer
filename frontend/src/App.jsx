import { useEffect, useState, useCallback, useMemo } from "react";
import { Menu, HeartPulse } from "lucide-react";
import Sidebar from "./components/Sidebar";
import StatCard from "./components/StatCard";
import PatientTable from "./components/PatientTable";
import MedicineTable from "./components/MedicineTable";
import EditMedicineModal from "./components/EditMedicineModal.jsx";
import * as api from "./api.js";
import EditPatientModal from "./components/EditPatientModal.jsx";

export default function App() {
  const [data, setData] = useState({
    patients: [],
    medicines: [],
  });

  const [ui, setUi] = useState({
    loading: true,
    sidebarOpen: false,
  });

  const loadData = useCallback(async () => {
    try {
      setUi((prev) => ({ ...prev, loading: true }));

      const [p, m] = await Promise.all([
        api.fetchPatients(),
        api.fetchMedicines(),
      ]);

      setData({
        patients: p.data,
        medicines: m.data,
      });
    } catch (err) {
      console.error("Failed to load data", err);
    } finally {
      setUi((prev) => ({ ...prev, loading: false }));
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleDelete = useCallback(async (type, id) => {
    const apiMap = {
      patients: api.deletePatient,
      medicines: api.deleteMedicine,
    };

    try {
      await apiMap[type](id);

      // safer + consistent with backend state
      await loadData();
    } catch (err) {
      alert(`Failed to delete ${type}`);
      console.error(err);
    }
  }, [loadData]);

  const [editingMedicine, setEditingMedicine] = useState(null);

  const handleEdit = (id) => {
  const med = data.medicines.find((m) => m.id === id);
  setEditingMedicine(med);
};
  const handleSave = async (updatedMed) => {
  try {
    await api.updateMedicine(updatedMed.id, updatedMed); // you’ll add this in api.js
    await loadData();
    setEditingMedicine(null);
  } catch (err) {
    console.error("Failed to update medicine", err);
  }
};

  const [editingPatient, setEditingPatient] = useState(null);

const handleEditPatient = (id) => {
  const patient = data.patients.find((p) => p.id === id);
  setEditingPatient(patient);
};

const handleSavePatient = async (updatedPatient) => {
  try {
    await api.updatePatient(updatedPatient.id, updatedPatient);
    await loadData();
    setEditingPatient(null);
  } catch (err) {
    console.error("Failed to update patient", err);
  }
};

  // ---------- Derived Stats (NO duplication) ----------
  const stats = useMemo(() => {
    const medicines = data.medicines;

    return {
      patients: data.patients.length,
      medicines: medicines.length,
      lowStock: medicines.filter((m) => (m.stock ?? 0) <= 10).length,
      expired: medicines.filter(
        (m) => m.expiry_date && new Date(m.expiry_date) < new Date()
      ).length,
    };
  }, [data]);



  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">

      {/* Sidebar */}
      <Sidebar
        isOpen={ui.sidebarOpen}
        setIsOpen={(val) =>
          setUi((prev) => ({ ...prev, sidebarOpen: val }))
        }
      />

      {/* Main */}
      <div className="flex-1 flex flex-col">

        {/* Mobile Header */}
        <header className="lg:hidden flex justify-between p-4 bg-white border-b sticky top-0 z-30">
          <div className="flex items-center gap-2 font-bold">
            <HeartPulse className="text-blue-600" size={20} />
            Patient Management System
          </div>

          <button
            onClick={() =>
              setUi((prev) => ({ ...prev, sidebarOpen: true }))
            }
            className="p-2 hover:bg-slate-100 rounded-xl"
          >
            <Menu size={24} />
          </button>
        </header>

        <main className="p-4 md:p-6 max-w-7xl mx-auto w-full space-y-8">

          {/* Header */}
          <section>
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="text-slate-500 text-sm">
              Overview of system activity
            </p>
          </section>

          {/* Stats */}
          <div className="grid sm:grid-cols-4 gap-4">
            <StatCard label="Patients" value={stats.patients} />
            <StatCard label="Medicines" value={stats.medicines} />
            <StatCard label="Low Stock" value={stats.lowStock} />
            <StatCard label="Expired" value={stats.expired} />
          </div>

          {/* Patients */}
          <TableSection title={`Patients (${stats.patients})`}>
            <PatientTable
              patients={data.patients}
              loading={ui.loading}
              onDelete={(id) => handleDelete("patients", id)}
              onEdit={handleEditPatient}
            />
            {editingPatient && (
  <EditPatientModal
    patient={editingPatient}
    onClose={() => setEditingPatient(null)}
    onSave={handleSavePatient}
  />
)}
          </TableSection>

          {/* Medicines */}
          <TableSection title={`Medicines (${stats.medicines})`}>
            <MedicineTable
              medicines={data.medicines}
              loading={ui.loading}
              onDelete={(id) => handleDelete("medicines", id)}
              onEdit={handleEdit}
            />
          </TableSection>

          {editingMedicine && (
  <EditMedicineModal
    medicine={editingMedicine}
    onClose={() => setEditingMedicine(null)}
    onSave={handleSave}
  />
)}


        </main>
      </div>
    </div>
  );
}

/* ---------- Reusable Section ---------- */

const TableSection = ({ title, children }) => (
  <section className="bg-white rounded-2xl border shadow-sm overflow-hidden">
    <div className="p-4 border-b bg-slate-50 font-semibold text-slate-700">
      {title}
    </div>
    {children}
  </section>
);