FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server/server.py .

# Expose port (Railway will provide PORT via env var)
EXPOSE 8000

# Run uvicorn with host 0.0.0.0 and port from PORT env var (default 8000)
# Railway will provide PORT environment variable at runtime
CMD python server.py

