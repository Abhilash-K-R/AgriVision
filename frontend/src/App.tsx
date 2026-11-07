import { Routes, Route, NavLink } from 'react-router-dom';
import { Camera, History, Info, ShieldCheck, Leaf } from 'lucide-react';
import CameraCapture from './components/CameraCapture';
import HistoryList from './components/HistoryList';
import About from './components/About';

export default function App() {
  return (
    <div className="min-h-screen bg-surface flex flex-col">
        {/* Professional Header */}
        <header className="bg-primary-dark text-white shadow-md sticky top-0 z-50">
          <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-primary p-2 rounded-xl text-white shadow-inner">
                <Leaf className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-lg font-bold tracking-tight">AgriVision</h1>
                <p className="text-xs text-emerald-200/80">Crop Disease Diagnostic Intelligence</p>
              </div>
            </div>
            <div className="flex items-center space-x-1 bg-emerald-950/40 px-3 py-1.5 rounded-full border border-emerald-800/50 text-xs text-emerald-300">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>v1.0.0 Preview</span>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-6">
          <Routes>
            <Route path="/" element={<CameraCapture />} />
            <Route path="/history" element={<HistoryList />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>

        {/* Bottom / Sticky Navigation for Mobile First Experience */}
        <nav className="bg-white border-t border-slate-200 sticky bottom-0 z-40 shadow-lg">
          <div className="max-w-4xl mx-auto px-6 py-3 flex justify-around">
            <NavLink
              to="/"
              className={({ isActive }) =>
                `flex flex-col items-center space-y-1 transition-colors ${
                  isActive ? 'text-primary font-semibold' : 'text-text-secondary hover:text-text'
                }`
              }
            >
              <Camera className="w-5 h-5" />
              <span className="text-xs">Diagnose</span>
            </NavLink>
            <NavLink
              to="/history"
              className={({ isActive }) =>
                `flex flex-col items-center space-y-1 transition-colors ${
                  isActive ? 'text-primary font-semibold' : 'text-text-secondary hover:text-text'
                }`
              }
            >
              <History className="w-5 h-5" />
              <span className="text-xs">History</span>
            </NavLink>
            <NavLink
              to="/about"
              className={({ isActive }) =>
                `flex flex-col items-center space-y-1 transition-colors ${
                  isActive ? 'text-primary font-semibold' : 'text-text-secondary hover:text-text'
                }`
              }
            >
              <Info className="w-5 h-5" />
              <span className="text-xs">About</span>
            </NavLink>
          </div>
        </nav>
    </div>
  );
}
