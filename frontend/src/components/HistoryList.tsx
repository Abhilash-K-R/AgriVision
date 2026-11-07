import { useEffect, useState } from "react";
import { api } from "../services/api";
import type { PredictionHistoryResponse, PredictionHistoryItem } from "../types";
import LoadingSpinner from "./LoadingSpinner";
import ErrorBanner from "./ErrorBanner";

function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

function classBadge(cls?: string | null): { label: string; cls: string } {
  if (!cls) return { label: "Rejected", cls: "bg-red-50 text-red-700 ring-red-200" };
  const map: Record<string, { label: string; cls: string }> = {
    healthy: { label: "Healthy", cls: "bg-green-50 text-green-700 ring-green-200" },
    early_blight: { label: "Early Blight", cls: "bg-amber-50 text-amber-800 ring-amber-200" },
    late_blight: { label: "Late Blight", cls: "bg-red-50 text-red-700 ring-red-200" },
  };
  return map[cls] ?? { label: cls, cls: "bg-gray-50 text-gray-700 ring-gray-200" };
}

export default function HistoryList() {
  const [data, setData] = useState<PredictionHistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api.history(page, 20)
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch((e: unknown) => {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load history");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [page]);

  return (
    <div className="space-y-4">
      <div className="card">
        <h1 className="text-xl font-semibold">Prediction history</h1>
        <p className="text-sm text-gray-600">Your recent scans and diagnoses.</p>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      {loading && <LoadingSpinner />}

      {!loading && data && (
        <>
          <div className="card p-0 overflow-hidden">
            <ul className="divide-y">
              {data.predictions.length === 0 && (
                <li className="p-6 text-sm text-gray-600">No predictions yet.</li>
              )}
              {data.predictions.map((item: PredictionHistoryItem) => {
                const badge = classBadge(item.disease_class ?? null);
                return (
                  <li key={item.prediction_id} className="flex items-center justify-between p-4">
                    <div className="flex items-center gap-3">
                      <span className={`rounded-lg px-2 py-1 text-xs font-medium ring-1 ${badge.cls}`}>
                        {badge.label}
                      </span>
                      <div>
                        <p className="text-sm font-medium">
                          {item.rejected ? "Rejected" : `${item.disease_class?.replace("_", " ") ?? "Unknown"}`}
                        </p>
                        <p className="text-xs text-gray-500">{formatDate(item.timestamp)}</p>
                      </div>
                    </div>
                    <div className="text-right text-xs text-gray-500">
                      {item.confidence != null && `${Math.round(item.confidence * 100)}% confidence`}
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>

          <div className="flex justify-between items-center">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="btn-secondary disabled:opacity-50"
            >
              Previous
            </button>
            <span className="text-sm text-gray-600">Page {page} of {Math.max(1, Math.ceil((data.total_count || 0) / 20))}</span>
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={page * 20 >= (data.total_count || 0)}
              className="btn-secondary disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}
