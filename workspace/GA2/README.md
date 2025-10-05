---
sdk: docker
app_port: 7167
description: deployment-ready-ga2-25c816
---

# Deployment observability API (Docker-based)

This Space runs a Dockerized FastAPI app (uvicorn) that exposes the observability endpoint.

Endpoints
- POST / or /latency  => accepts {"regions": [...], "threshold_ms": <number>} and returns per-region metrics.
