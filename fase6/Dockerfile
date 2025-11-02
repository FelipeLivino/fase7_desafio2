# Use a slim Python base image
FROM python:3.10-slim

# Install git, which is required for torch.hub.load with a local repository
RUN apt-get update && apt-get install -y git

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install PyTorch (CPU version) and other dependencies.
# Using the official index URL for torch is recommended.
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# This includes the model (.pt file) and the images
COPY . .

# Command to run the detection script
CMD ["python", "run_detection.py"]
