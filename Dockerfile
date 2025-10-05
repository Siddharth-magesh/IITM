FROM python:3.11-slim

# Create a non-root user with UID 1000
RUN useradd --create-home --uid 1000 appuser

WORKDIR /home/appuser/app

# Copy application files
COPY requirements.txt ./requirements.txt
COPY main.py ./main.py
COPY q-vercel-latency.json ./q-vercel-latency.json

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER appuser

ENV APP_PORT=7167
EXPOSE 7167

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${APP_PORT}"]
