FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY static/ ./static/
COPY templates/ ./templates/

# Create non-root user and set ownership
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Flask configuration
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000
CMD ["python", "-m", "flask", "run"]
