FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Command to run both the FastAPI server and the Kafka consumer
# For production, it's better to run them as separate containers, 
# but for local dev we can start the API by default.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
