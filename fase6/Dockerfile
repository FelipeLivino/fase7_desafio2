# Use a slim Python base image
FROM python:3.10-slim

# Install git and essential multimedia libraries
RUN apt-get update && apt-get install -y git libgl1 libglib2.0-0 && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make the startup script executable
COPY start.sh .
RUN chmod +x start.sh

# Expose the port Streamlit will run on
EXPOSE 8501

# Set the command to run the startup script
CMD ["./start.sh"]
