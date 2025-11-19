FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies required to build some Python packages (e.g. asyncpg)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   gcc \
	   libpq-dev \
	   build-essential \
	   curl \
	&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create non-root user and set permissions
RUN useradd --create-home appuser \
	&& mkdir -p /app \
	&& chown -R appuser:appuser /app

# Copy application code
COPY . /app
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 80

# Default command: run Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
