# Stage 1: Build dependencies as wheels
FROM python:3.10-slim AS builder

WORKDIR /wheels

# Copy requirements
COPY requirements.txt .

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Build wheels
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.10-slim

WORKDIR /app

# Copy wheels from builder stage
COPY --from=builder /wheels /wheels

# Install the wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && \
    rm -rf /wheels

# Copy the application
COPY . .

# Create necessary directories
RUN mkdir -p app/static/css app/static/js app/templates personas

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 7860

# Command to run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]