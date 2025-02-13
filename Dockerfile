FROM python:3.9-slim

# Install pip and dependencies
RUN apt-get update && apt-get install -y python3-pip

# Set the working directory
WORKDIR /app

# Copy your code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
