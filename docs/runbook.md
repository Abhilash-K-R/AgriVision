# AgriVision Runbook

This document provides troubleshooting guidance for common issues, log inspection, and service restart procedures.

## Table of Contents
- [Common Errors](#common-errors)
- [Checking Logs](#checking-logs)
- [Restarting the Service](#restarting-the-service)

## Common Errors

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `413 Request Entity Too Large` | Image upload exceeds `max_image_size_mb` (default: 5MB) | Reduce image size or increase `max_image_size_mb` in `.env` |
| `500 Internal Server Error` | Model not loaded or inference failure | Check that ONNX model exists at the path configured in `MODEL_PATH` |
| `connection refused` | Backend not running | Start the backend server |
| `422 Validation Error` | Invalid input format | Ensure image is a valid JPEG/PNG file |

## Checking Logs

The application uses structured JSON-like logs with request ID correlation. Logs appear in the following format:

```
2024-01-15T10:30:45 | INFO | backend.app.api.router | request_id=abc123def456 | Prediction completed
2024-01-15T10:30:45 | INFO | backend.app.api.router | request_id=abc123def456 | predicted_class=early_blight, confidence=0.92
```

### Viewing Logs

**Local development:**
```bash
# Using uvicorn directly
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Or via docker-compose
cd ..\..  # project root
docker compose logs -f backend
```

**Production/Render:**
```bash
# Check Render dashboard logs
# Or SSH into your instance and run:
journalctl -u your-service --since "1 hour ago"
```

### Filtering by Request ID

To find all logs for a specific request, search by the `request_id` field:

```bash
# grep example
grep "request_id=abc123def456" backend/logs/app.log

# Or if using docker compose
docker compose logs backend | grep "request_id=abc123def456"
```

The request ID is also available in the `X-Request-ID` response header.

## Restarting the Service

### Local Development

```bash
# Stop the running process (Ctrl+C)
# Restart
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Docker Compose

```bash
# Restart the backend service only
docker compose restart backend

# Or rebuild and restart if code changes
docker compose up -d --build backend
```

### Using Render Dashboard

1. Go to your Render service dashboard
2. Click "Restart Service" button
3. Or deploy a new commit to trigger a fresh deployment

## Health Checks

- **Liveness:** `GET /api/v1/health` - Returns service health status
- **Readiness:** Same endpoint - checks database and model connectivity

## Debugging Tips

1. If predictions are always rejected, check the `confidence_threshold` setting (default: 0.70) in `.env`
2. If logs show `request_id=N/A`, the RequestIdMiddleware may not be firing - ensure it's the first middleware in `main.py`
3. For slow predictions, check GPU availability or model size in the logs