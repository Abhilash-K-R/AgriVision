import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = dirname(fileURLToPath(import.meta.url));

// The API base URL is read from the environment at build time so the same
// frontend artifact can point at a staging or production backend.
const apiBaseUrl = process.env.VITE_API_URL ?? "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      // In dev, forward /api/* to the FastAPI backend so the browser never
      // sees a cross-origin request. This keeps CORS simple on the backend.
      "/api": {
        target: apiBaseUrl,
        changeOrigin: true,
        secure: false,
      },
    },
  },
  resolve: {
    alias: {
      "@": resolve(rootDir, "src"),
    },
  },
  build: {
    // Mobile-first app: keep the JS payload small for slow connections.
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        manualChunks: {
          react: ["react", "react-dom"],
          router: ["react-router-dom"],
        },
      },
    },
  },
});