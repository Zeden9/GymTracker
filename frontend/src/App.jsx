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

    const minVolume = Math.min(...volumeData.map((p) => p.volume));
    const yMin = Math.floor(minVolume * 0.9);
    chartRef.current = new ChartJS(canvasRef.current, {
      type: "line",
      data: {
        labels: volumeData.map((p) => p.workout_date),
        datasets: [{
          label: "Volume (kg × reps)",
          data: volumeData.map((p) => p.volume),
          borderColor: "#6366f1",
          backgroundColor: "rgba(99,102,241,0.08)",
          fill: true,
          tension: 0,
          pointRadius: 4,
          pointHoverRadius: 6,
          borderWidth: 2,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.parsed.y.toLocaleString("en-EN")} kg×reps`,
            },
          },
        },
        scales: {
          y: {
            min: yMin,  
            suggestedMin: undefined,
            title: { display: true, text: "Volume", font: { size: 13 } },
            ticks: { font: { size: 12 } },
          },
          x: {
            title: { display: true, text: "Date", font: { size: 13 } },
            ticks: { font: { size: 12 } },
          },
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

  const selectedExercise = exercises.find((e) => e.id === selectedId);
  const selectedName = selectedExercise?.name ?? "";
  const selectedDescription = selectedExercise?.description ?? "test";

  return (
    <div style={{ width: "70%", maxWidth: 1200, margin: "40px auto", padding: "0 40px", fontFamily: "sans-serif", boxSizing: "border-box" }}>
      <h1 style={{ fontSize: 26, marginBottom: 32, fontWeight: 600 }}>Training progress</h1>

      {/* Dropdown */}
      <div style={{ marginBottom: 28 }}>
        <label style={{ display: "block", marginBottom: 8, fontSize: 14, color: "#555", fontWeight: 500 }}>
          Exercise
        </label>
        <select
          value={selectedId ?? ""}
          onChange={(e) => setSelectedId(Number(e.target.value))}
          style={{
            width: 280,
            padding: "10px 12px",
            fontSize: 15,
            borderRadius: 8,
            border: "1px solid #ccc",
            background: "transparent",
            color: "inherit",
            colorScheme: "light dark",  // ← naprawia białe opcje w dark mode
          }}
        >
          {exercises.map((ex) => (
            <option key={ex.id} value={ex.id}>{ex.name}</option>
          ))}
        </select>
      </div>

      {/* Wykres */}
      {loading && <p style={{ color: "#888" }}>Loading...</p>}

      {!loading && volumeData.length === 0 && (
        <p style={{ color: "#888" }}>No data for this exercise.</p>
      )}

      {!loading && volumeData.length > 0 && (
        <>
          <h2 style={{ fontSize: 17, marginBottom: 20, fontWeight: 500, color: "inherit" }}>
            {selectedName} — Training volume
          </h2>
          <div style={{ width: "100%", height: 340 }}>
            <canvas ref={canvasRef} />
          </div>
        </>
      )}

      {/* Opis pod wykresem */}
      {!loading && selectedName && (
        <div style={{
          marginTop: 32,
          background: "transparent",
          border: "1px solid #e5e5e5",
          borderRadius: 10,
          padding: "16px 20px",
        }}>
          <div style={{ fontSize: 12, color: "#888", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.05em" }}>
            Description
          </div>
          <p style={{ fontSize: 14, color: "inherit", margin: 0, lineHeight: 1.6 }}>
            {selectedDescription}
          </p>
        </div>
      )}

    </div>
  );
}