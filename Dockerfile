# Use an official Python image as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

RUN pip install --no-cache-dir jupyterlab && \
    pip install --no-cache-dir -r requirements.txt

# Copy the requirements file and install other dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code of the application to the container
COPY . .

# Expose port 8888 for Jupyter Lab
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--LabApp.token=''"]