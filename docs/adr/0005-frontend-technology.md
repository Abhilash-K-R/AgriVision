# ADR 0005: React with Vite

## Status
Accepted

## Context
AgriVision's frontend must be mobile-first, lightweight, and easy to deploy. The target devices are farmers' smartphones (Android/iOS) and low-cost tablets. The deployment target is Vercel, which has first-class support for React projects.

## Decision
We choose **React 18** powered by **Vite** as the build tool and development server.

### Tooling Stack:
- **React 18** with functional components and hooks (`useState`, `useEffect`)
- **Vite** for dev server ( instant start, HMR) and build (optimized chunks)
- **Tailwind CSS** for utility-first styling (mobile-first breakout points)
- **Axios** for API client communication (to FastAPI backend)
- **React Router** for page navigation (upload, camera, result, history)
- **Lucide React** for icon set (lightweight, consistent styling)

### Deployment:
- `vercel` CLI deploys `frontend/` directory on every git push.
- Environment variables (API endpoint, model path) injected via Vercel dashboard.

## Alternatives Considered

| Option | Reason |
|---|---|
| **Create React App (CRA)** | Still used, but deprecated in favor of Vite; CRA has slower build times and no config tweakability. |
| **Next.js** | Excellent for SSR, but overkill for AgriVision; the app is primarily a single-page image upload flow. Extra complexity not needed for v1. |
| **Flutter / React Native** | Native mobile apps require app store deployment and native builds; AgriVision v1 is web-first for fastest farmer access (no install barrier). |
| **Plain HTML/JS** | Fastest to start, but lacks component reusability, state management, and type safety as the app grows. |

## Consequences
### Positive:
- **Instant dev experience:** Vite HMR (Hot Module Replacement) means seeing image upload changes instantly without full page reload.
- **Small bundle:** Vite's optimized output and Tree-shaking keep the JS bundle small; important for mobile data caps.
- **Vercel integration:** Zero-config deploys; preview URLs on every PR for stakeholder testing.
- **Mobile-first Tailwind:** Utility classes like `sm:` and `md:` make responsive layouts straightforward.

### Negative / Trade-offs:
- **SEO:** React SPA has poor out-of-the-box SEO; mitigated by adding meta tags and potentially Vercel Server Functions later.
- **State management:** For v1, local component state is sufficient; adding Redux or Zustand would be premature, but could be added if feedback flow becomes complex.
---