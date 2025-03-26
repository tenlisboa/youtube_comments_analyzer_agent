FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user to run the application
RUN useradd -m appuser
USER appuser

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py", "--server", "--port", "8000"]
