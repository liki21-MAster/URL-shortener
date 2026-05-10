# Stage 1: The Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: The Production Image
FROM python:3.11-slim
WORKDIR /app

# Copy the installed dependencies from Stage 1
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# COPY YOUR FILE (Changed from main.py)
COPY main.py .

# Expose the application port
EXPOSE 8000

# START THE SERVER (Changed from main:app to main:app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]