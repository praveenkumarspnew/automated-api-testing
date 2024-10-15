# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Ensure the .env file is included in the build
COPY .env .env

# Run the script to generate API tests, and then run pytest
CMD ["sh", "-c", "python generate_api_tests.py && pytest tests/test_auto_generated.py"]

