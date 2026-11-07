# AgriVision Frontend

Mobile-first React + Vite PWA for tomato disease diagnosis.

## Run locally

```bash
npm install
npm run dev
```

Set `VITE_API_URL` in `.env` to point at your FastAPI backend.

## Build

```bash
npm run build
npm run preview
```

## Project structure

- `src/components/` - UI components
- `src/services/api.ts` - fetch client to FastAPI
- `src/types/index.ts` - TypeScript types matching backend schemas
