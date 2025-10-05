---
sdk: docker
app_port: 7167
description: deployment-ready-ga2-25c816
---

# Deployment observability API (Docker-based)

This project provides a Dockerized FastAPI application that exposes an observability endpoint. The main purpose is to calculate and return per-region latency metrics.

Verification number: 41733674

This Space runs a Dockerized FastAPI app (uvicorn) that exposes the observability endpoint.

Endpoints
- POST / or /latency  => accepts {"regions": [...], "threshold_ms": <number>} and returns per-region metrics.
# IITM
Assignments and Projects

## Project Structure

*   `docs/`: Contains documentation for the project.
*   `workspace/`: Contains the main application code.
*   `LICENSE`: The license for the project.
*   `README.md`: This file.
*   `requirements.txt`: The python dependencies for the project.
