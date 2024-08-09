# Use the latest Python image
FROM python:latest

# Set the working directory to the root
WORKDIR /

# Copy the requirements file from the archive directory to the root directory in the Docker container
COPY requirements.txt /requirements.txt

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Copy the application files to the root directory
COPY archive.py /

# Set environment variables
ENV PORT=5439 HOST=0.0.0.0

# Expose port 5439 (this is for the application, not for S3)
EXPOSE 5439

# Command to run
CMD ["python3", "./archive.py"]