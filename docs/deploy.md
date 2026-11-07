# Deployment Guide: AgriVision

## Frontend (Vercel)
1. Push your code to a GitHub repository.
2. Sign into [Vercel](https://vercel.com/) and import your project.
3. Configure settings:
   - Framework Preset: Vite
   - Root Directory: `frontend/`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Set Environment Variables (`VITE_API_URL`).
5. Deploy.

## Backend (Render)
1. Create a new "Web Service" on [Render](https://render.com/).
2. Connect your GitHub repository.
3. Configure settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. Set Environment Variables:
   - `DATABASE_URL`: Connection string from Neon PostgreSQL.
   - `SECRET_KEY`: A secure random string.

## Security Considerations
- Ensure `CORS_ORIGINS` is set correctly to your frontend domain in the backend environment variables.
- Use strong, unique secrets for database connections and application keys.