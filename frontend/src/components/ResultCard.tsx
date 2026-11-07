import { CheckCircle2, XCircle, Leaf, AlertTriangle, ThumbsUp, ThumbsDown } from "lucide-react";
import { useState } from "react";
import type { DiagnosisResponse } from "../types";
import { api } from "../services/api";
import ErrorBanner from "./ErrorBanner";

interface Props {
  result: DiagnosisResponse;
  onFeedback?: () => void;
}

const diseaseStyles: Record<string, { label: string; color: string }> = {
  healthy: { label: "Healthy", color: "text-green-700 bg-green-50 ring-green-200" },
  early_blight: { label: "Early Blight", color: "text-amber-800 bg-amber-50 ring-amber-200" },
  late_blight: { label: "Late Blight", color: "text-red-700 bg-red-50 ring-red-200" },
};

export function ResultCard({ result, onFeedback }: Props) {
  const [feedbackSent, setFeedbackSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const isRejected = result.rejected;
  const disease = result.disease_class ?? null;
  const style = disease ? diseaseStyles[disease] : null;
  const confidence = result.confidence;

  const submitFeedback = async (isCorrect: boolean) => {
    setLoading(true);
    setError(null);
    try {
      await api.feedback({
        prediction_id: result.prediction_id,
        is_correct: isCorrect,
      });
      setFeedbackSent(true);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to submit feedback");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      <div className="flex items-start gap-3">
        {isRejected ? (
          <XCircle className="h-5 w-5 text-red-600 mt-0.5" />
        ) : disease === "healthy" ? (
          <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5" />
        ) : (
          <AlertTriangle className="h-5 w-5 text-amber-600 mt-0.5" />
        )}
        <div className="flex-1">
          <h2 className="text-lg font-semibold">
            {isRejected ? "Prediction rejected" : "Diagnosis result"}
          </h2>
          <p className="text-sm text-gray-600">
            {new Date(result.timestamp).toLocaleString()}
          </p>
        </div>
      </div>

      {isRejected ? (
        <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800">
          <p className="font-medium">Could not confidently diagnose</p>
          <p className="mt-1">{result.rejection_reason ?? "Low confidence or non-tomato image."}</p>
          <p className="mt-2 text-xs">Tip: Ensure good lighting, focus on a single leaf, and avoid heavy shadows.</p>
        </div>
      ) : (
        <>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <div className={`rounded-xl ring-1 p-4 ${style?.color ?? ""}`}>
              <div className="flex items-center gap-2">
                <Leaf className="h-4 w-4" />
                <span className="text-sm font-medium">Predicted class</span>
              </div>
              <p className="mt-1 text-xl font-semibold capitalize">{disease?.replace("_", " ")}</p>
            </div>
            <div className="rounded-xl bg-gray-50 ring-1 ring-gray-200 p-4">
              <p className="text-sm font-medium text-gray-600">Confidence</p>
              <div className="mt-2 flex items-end gap-2">
                <p className="text-2xl font-semibold">{confidence !== null ? Math.round(confidence * 100) : 0}%</p>
                <div className="mb-1 h-2 w-24 rounded bg-gray-200 overflow-hidden">
                  <div
                    className="h-full bg-green-600"
                    style={{ width: `${Math.max(0, Math.min(100, (confidence ?? 0) * 100))}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {result.care_advice && (
            <div className="mt-4 rounded-xl bg-blue-50 ring-1 ring-blue-200 p-4 text-sm">
              <p className="font-medium text-blue-900">Care advice</p>
              <p className="mt-1 whitespace-pre-wrap text-blue-800">{result.care_advice}</p>
            </div>
          )}

          {!feedbackSent ? (
            <div className="mt-4 flex items-center gap-3">
              <span className="text-sm text-gray-600">Was this correct?</span>
              <button
                onClick={() => submitFeedback(true)}
                disabled={loading}
                className="btn-secondary flex items-center gap-1"
              >
                <ThumbsUp className="h-4 w-4" />
                Yes
              </button>
              <button
                onClick={() => submitFeedback(false)}
                disabled={loading}
                className="btn-secondary flex items-center gap-1"
              >
                <ThumbsDown className="h-4 w-4" />
                No
              </button>
            </div>
          ) : (
            <div className="mt-4 text-sm text-green-700">
              Thank you for your feedback!
            </div>
          )}
        </>
      )}

      {onFeedback && (
        <button onClick={onFeedback} className="btn-secondary mt-4">
          New scan
        </button>
      )}
    </div>
  );
}
