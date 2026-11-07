import React, { useEffect, useState, useRef } from 'react';
import { Camera, Upload, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import type { DiagnosisResponse } from '../types';
import LoadingSpinner from './LoadingSpinner';
import ErrorBanner from './ErrorBanner';
import { ResultCard } from './ResultCard';

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : 'An unexpected error occurred.';
}

export default function CameraCapture() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DiagnosisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError('Image must be 5 MB or smaller.');
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setError(null);
  };

  const handleDiagnose = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const data = await api.predict(selectedFile);
      setResult(data);
    } catch (err: unknown) {
      setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="space-y-6">
      {/* Hero card */}
      <div className="card bg-gradient-to-br from-emerald-900 to-primary text-white shadow-xl">
        <h2 className="text-xl font-bold mb-2">Tomato Leaf Disease Diagnosis</h2>
        <p className="text-emerald-100 text-sm leading-relaxed">
          Photograph or upload a clear image of a tomato leaf. Our AI model instantly evaluates health status and recommends tailored treatment advice.
        </p>
      </div>

      {error && <ErrorBanner message={error} />}

      {/* Upload / Capture Section */}
      {!previewUrl ? (
        <div className="card border-2 border-dashed border-slate-300 hover:border-primary transition-colors text-center py-12 px-6">
          <div className="max-w-xs mx-auto space-y-4">
            <div className="w-16 h-16 bg-emerald-50 text-primary rounded-full flex items-center justify-center mx-auto shadow-sm">
              <Camera className="w-8 h-8" />
            </div>
            <div>
              <h3 className="font-semibold text-text">Upload or Capture Leaf</h3>
              <p className="text-xs text-text-secondary mt-1">Supports JPG, PNG (Max 5MB)</p>
            </div>
            <div className="flex gap-3 justify-center pt-2">
              <button
                onClick={() => fileInputRef.current?.click()}
                className="btn-primary flex items-center gap-2 text-sm w-full justify-center"
              >
                <Upload className="w-4 h-4" />
                Select Photo
              </button>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              capture="environment"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="card overflow-hidden p-0">
            <div className="relative aspect-video bg-slate-900 flex items-center justify-center">
              <img src={previewUrl} alt="Leaf preview" className="max-h-80 w-full object-contain" />
              <button
                onClick={handleReset}
                className="absolute top-4 right-4 bg-slate-900/80 hover:bg-slate-900 text-white p-2 rounded-full shadow transition-colors"
                title="Retake photo"
              >
                <RefreshCw className="w-5 h-5" />
              </button>
            </div>

            {!result && !loading && (
              <div className="p-6 bg-white flex justify-end">
                <button onClick={handleDiagnose} className="btn-primary w-full flex items-center justify-center gap-2">
                  <Camera className="w-5 h-5" />
                  Run Diagnosis
                </button>
              </div>
            )}
          </div>

          {loading && <LoadingSpinner />}

          {/* Result Card */}
          {result && (
            <ResultCard
              result={result}
              onFeedback={handleReset}
            />
          )}
        </div>
      )}
    </div>
  );
}
