import { useEffect, useState, useRef } from "react";
import {
  Chart as ChartJS,
  LineController,
  CategoryScale, LinearScale,
  PointElement, LineElement,
  Tooltip, Filler,
} from "chart.js";

ChartJS.register(LineController, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler);

const API = "http://localhost:8000";

export default function App() {
  const [exercises, setExercises] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [volumeData, setVolumeData] = useState([]);
  const [loading, setLoading] = useState(false);
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    fetch(`${API}/exercises`)
      .then((r) => r.json())
      .then((data) => {
        setExercises(data);
        if (data.length > 0) setSelectedId(data[0].id);
      });
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    setVolumeData([]);
    setLoading(true);
    fetch(`${API}/exercises/${selectedId}/volume`)
      .then((r) => r.json())
      .then((data) => {
        setVolumeData(data);
        setLoading(false);
      });
  }, [selectedId]);

  useEffect(() => {
    if (!canvasRef.current || volumeData.length === 0) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    chartRef.current = new ChartJS(canvasRef.current, {
      type: "line",
      data: {
        labels: volumeData.map((p) => p.workout_date),
        datasets: [{
          label: "Objętość (kg × powt.)",
          data: volumeData.map((p) => p.volume),
          borderColor: "#6366f1",
          backgroundColor: "rgba(99,102,241,0.1)",
          fill: true,
          tension: 0.4,
          pointRadius: 5,
          pointHoverRadius: 7,
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.parsed.y.toLocaleString("pl-PL")} kg×powt.`,
            },
          },
        },
        scales: {
          y: { beginAtZero: true, title: { display: true, text: "Objętość" } },
          x: { title: { display: true, text: "Data treningu" } },
        },
      },
    });

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
        chartRef.current = null;
      }
    };
  }, [volumeData]);

  const selectedName = exercises.find((e) => e.id === selectedId)?.name ?? "";

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", padding: "0 20px", fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 22, marginBottom: 24 }}>Postęp treningowy</h1>

      <label style={{ display: "block", marginBottom: 8, fontSize: 14, color: "#555" }}>
        Ćwiczenie
      </label>
      <select
        value={selectedId ?? ""}
        onChange={(e) => setSelectedId(Number(e.target.value))}
        style={{ padding: "8px 12px", fontSize: 15, borderRadius: 8, border: "1px solid #ccc", marginBottom: 32 }}
      >
        {exercises.map((ex) => (
          <option key={ex.id} value={ex.id}>{ex.name}</option>
        ))}
      </select>

      {loading && <p style={{ color: "#888" }}>Ładowanie...</p>}

      {!loading && volumeData.length === 0 && (
        <p style={{ color: "#888" }}>Brak danych dla tego ćwiczenia.</p>
      )}

      {!loading && volumeData.length > 0 && (
        <>
          <h2 style={{ fontSize: 16, marginBottom: 16, fontWeight: 500 }}>
            {selectedName} — objętość treningowa
          </h2>
          <canvas ref={canvasRef} />
        </>
      )}
    </div>
  );
}