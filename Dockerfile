FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir .[postgres]

COPY . .

# Create a non-root user to run the application
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser

CMD ["python", "main.py"]