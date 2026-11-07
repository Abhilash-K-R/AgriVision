import { ShieldCheck, Database, BrainCircuit, Globe } from 'lucide-react';

export default function About() {
  return (
    <div className="space-y-6">
      <div className="card bg-white space-y-4">
        <h2 className="text-2xl font-bold text-text">About AgriVision</h2>
        <p className="text-text-secondary text-sm leading-relaxed">
          AgriVision is a professional-grade diagnostic platform designed to bridge the gap between
          complex computer vision and practical farm management. Our mission is to empower farmers
          with instant, actionable intelligence to protect crop yields.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card bg-white p-6 space-y-3 border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
          <div className="bg-primary/10 w-10 h-10 rounded-xl flex items-center justify-center text-primary">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-text">Neural Engine</h3>
          <p className="text-xs text-text-secondary leading-relaxed">
            Powered by a MobileNetV2 architecture optimized for low-latency, mobile-first inference via ONNX Runtime.
          </p>
        </div>

        <div className="card bg-white p-6 space-y-3 border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
          <div className="bg-primary/10 w-10 h-10 rounded-xl flex items-center justify-center text-primary">
            <Database className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-text">Data Provenance</h3>
          <p className="text-xs text-text-secondary leading-relaxed">
            Validated against the PlantVillage dataset using leak-free train/test splitting for verified production accuracy.
          </p>
        </div>

        <div className="card bg-white p-6 space-y-3 border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
          <div className="bg-primary/10 w-10 h-10 rounded-xl flex items-center justify-center text-primary">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-text">Production Grade</h3>
          <p className="text-xs text-text-secondary leading-relaxed">
            FastAPI backend with structured logging, rate limiting, and CI/CD quality gates for high availability.
          </p>
        </div>

        <div className="card bg-white p-6 space-y-3 border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
          <div className="bg-primary/10 w-10 h-10 rounded-xl flex items-center justify-center text-primary">
            <Globe className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-text">Open Access</h3>
          <p className="text-xs text-text-secondary leading-relaxed">
            Designed to work in low-connectivity farm environments via lightweight PWA caching and mobile optimization.
          </p>
        </div>
      </div>

      <div className="text-center py-4">
        <p className="text-[10px] text-text-secondary italic uppercase tracking-widest">
          AgriVision v1.0.0 © 2026 • Professional Crop Intelligence
        </p>
      </div>
    </div>
  );
}
