# ── Base image ───────────────────────────────────────────────
FROM python:3.10-slim

# ── System deps ──────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────
WORKDIR /app

# ── Copy requirements first (layer cache optimization) ────────
COPY requirements.txt .

# ── Install Python dependencies ───────────────────────────────
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy the full project ─────────────────────────────────────
COPY . .

# ── Streamlit config ──────────────────────────────────────────
RUN mkdir -p /app/.streamlit
COPY .streamlit/config.toml /app/.streamlit/config.toml

# ── Expose port ───────────────────────────────────────────────
EXPOSE 8501

# ── Health check ──────────────────────────────────────────────
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ── Launch command ────────────────────────────────────────────
CMD ["streamlit", "run", "Dashboard/App.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]