import { RefreshCw } from 'lucide-react';

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center p-12 card animate-pulse bg-white border border-slate-100">
      <RefreshCw className="w-10 h-10 text-primary animate-spin mb-4" />
      <span className="text-sm font-semibold text-text">Analyzing leaf imagery...</span>
      <p className="text-xs text-text-secondary mt-1 text-center max-w-[200px]">
        Running neural network inference with ONNX Runtime
      </p>
    </div>
  );
}
