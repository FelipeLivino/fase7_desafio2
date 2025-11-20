# Use a slim Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install dos2unix and fix CRLF issues
RUN apt-get update && apt-get install -y dos2unix \
    && dos2unix /app/start.sh

# Make the start script executable
RUN chmod +x /app/start.sh

# Expose the ports for the backend (8000) and frontend (8501)
EXPOSE 8004
EXPOSE 8504

# Command to run the start script
CMD ["./start.sh"]
