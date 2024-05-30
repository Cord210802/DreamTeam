# Use an official Python image as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code of the application to the container
COPY . .

# Copy the start.sh script
COPY start.sh .

# Make the start.sh script executable
RUN chmod +x start.sh

# Run the start.sh script when the container starts
CMD ["./start.sh"]