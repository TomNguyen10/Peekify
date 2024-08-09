# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container at /app
COPY app /app

# Copy the .env file into the container at /app (optional if using Docker Compose or `--env-file`)
COPY .env /app

# Expose port 80 for the FastAPI application
EXPOSE 80

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
