FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install python dependencies
# Note: In production, we'd copy requirements directly or use poetry/pipenv.
RUN pip install --no-cache-dir -e .

EXPOSE 8501
CMD ["streamlit", "run", "app/Home.py", "--server.address=0.0.0.0"]
