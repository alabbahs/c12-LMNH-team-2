# Use the official Python base image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install  -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Set environment variables for Streamlit
ENV STREAMLIT_PORT 8501
ENV STREAMLIT_ADDRESS 0.0.0.0

# Expose the Streamlit port
EXPOSE ${STREAMLIT_PORT}

# Command to run the application
CMD ["streamlit", "run", "streamlit.py"]