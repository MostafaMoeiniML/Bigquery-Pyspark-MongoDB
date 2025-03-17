# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script and data files
COPY ingest.py .
COPY amazon_review.csv .
# Copy credentials file with a fixed name
COPY big-test-449715-2b0e9010365e.json credentials.json

# Run ingest.py when the container launches
CMD ["python", "ingest.py"]